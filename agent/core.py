"""Main agent loop orchestrator — runs the self-improvement cycle."""

import json
import time
from datetime import datetime, timezone

import anthropic
from dotenv import load_dotenv

from agent.screener import screen_agents, DEFAULT_SCREENING_PROMPT
from agent.evaluator import score, get_failures, load_test_set, load_ground_truth_labels
from agent.improver import rewrite
from agent.memory import (
    AgentState, load_state, save_state, hash_prompt, append_to_agent_log,
)
from chain.filecoin import store_iteration_log, load_state_from_filecoin, update_state_on_filecoin
from chain.agentproof import submit_performance
from chain.celo import get_celo_tx_url

load_dotenv()


def run_improvement_loop(max_iterations: int = 100, resume: bool = True):
    """Run the autonomous self-improvement loop.

    Each iteration:
    1. Evaluate current screening logic
    2. Log to Filecoin
    3. Update ERC-8004 TrustScore via AgentProof
    4. Analyse failures
    5. Improve via Anthropic API
    6. Guardrail: don't apply if worse
    7. Persist state to Filecoin
    8. Log to agent_log.json
    """
    client = anthropic.Anthropic()

    # Load or initialize state
    if resume:
        state = load_state()
        if state.iteration > 0:
            print(f"Resuming from iteration {state.iteration}")
    else:
        state = AgentState()

    if not state.current_prompt:
        state.current_prompt = DEFAULT_SCREENING_PROMPT
        state.best_prompt = DEFAULT_SCREENING_PROMPT

    # Load eval data
    test_set = load_test_set()
    ground_truth = load_ground_truth_labels()

    print(f"Starting improvement loop: {state.iteration} -> {max_iterations}")
    print(f"Eval set size: {len(test_set)} agents")
    print("-" * 60)

    for i in range(state.iteration, max_iterations):
        iter_start = time.time()
        timestamp = datetime.now(timezone.utc).isoformat()

        # 1. EVALUATE current screening logic
        print(f"\n[Iteration {i}] Screening {len(test_set)} agents...")
        predictions = screen_agents(test_set, prompt=state.current_prompt, client=client)
        accuracy = score(predictions, ground_truth)
        print(f"[Iteration {i}] Accuracy: {accuracy:.1%}")

        # Track best
        if accuracy > state.best_accuracy:
            state.best_accuracy = accuracy
            state.best_prompt = state.current_prompt
            print(f"[Iteration {i}] New best accuracy!")

        # 2. LOG to Filecoin
        log_entry = {
            "iteration": i,
            "accuracy": accuracy,
            "prompt_hash": hash_prompt(state.current_prompt),
            "timestamp": timestamp,
            "predictions_count": len(predictions),
            "tx_hash": None,
            "filecoin_cid": None,
        }

        try:
            filecoin_cid = store_iteration_log(log_entry)
            log_entry["filecoin_cid"] = filecoin_cid
            state.filecoin_cids.append(filecoin_cid)
            print(f"[Iteration {i}] Stored on Filecoin: {filecoin_cid}")
        except Exception as e:
            print(f"[Iteration {i}] Filecoin storage failed: {e}")

        # 3. UPDATE ERC-8004 TrustScore via AgentProof
        try:
            tx_hash = submit_performance(accuracy, log_entry.get("filecoin_cid"))
            log_entry["tx_hash"] = tx_hash
            state.tx_hashes.append(tx_hash)
            print(f"[Iteration {i}] TrustScore updated: {tx_hash}")
            print(f"[Iteration {i}] Explorer: {get_celo_tx_url(tx_hash)}")
        except Exception as e:
            print(f"[Iteration {i}] AgentProof update failed: {e}")

        # 4. ANALYSE failures
        failures = get_failures(predictions, ground_truth)
        print(f"[Iteration {i}] Failures: {len(failures)}/{len(predictions)}")

        # 5. IMPROVE via Anthropic API
        if failures:
            print(f"[Iteration {i}] Generating improved prompt...")
            new_prompt = rewrite(
                current_prompt=state.current_prompt,
                failures=failures,
                iteration=i,
                accuracy=accuracy,
                client=client,
            )

            # 6. GUARDRAIL: don't apply if worse
            print(f"[Iteration {i}] Testing new prompt...")
            new_predictions = screen_agents(test_set, prompt=new_prompt, client=client)
            new_accuracy = score(new_predictions, ground_truth)
            print(f"[Iteration {i}] New accuracy: {new_accuracy:.1%}")

            if new_accuracy >= accuracy:
                state.current_prompt = new_prompt
                print(f"[Iteration {i}] Prompt updated! {accuracy:.1%} -> {new_accuracy:.1%}")
            else:
                print(f"[Iteration {i}] New prompt worse ({new_accuracy:.1%} < {accuracy:.1%}), keeping current")
        else:
            print(f"[Iteration {i}] Perfect score — no improvement needed")

        # 7. PERSIST state
        state.iteration = i + 1
        state.accuracy_history.append(accuracy)
        state.prompt_hashes.append(hash_prompt(state.current_prompt))
        save_state(state)

        try:
            update_state_on_filecoin(state)
        except Exception as e:
            print(f"[Iteration {i}] Filecoin state update failed: {e}")

        # 8. LOG to agent_log.json
        log_entry["elapsed_seconds"] = round(time.time() - iter_start, 2)
        log_entry["decision"] = "prompt_updated" if failures and new_accuracy >= accuracy else "prompt_kept"
        log_entry["tool_calls"] = [
            "anthropic_api:screen",
            "filecoin:store",
            "agentproof:submit_performance",
            "anthropic_api:rewrite",
        ]
        append_to_agent_log(log_entry)

        print(f"[Iteration {i}] Complete ({log_entry['elapsed_seconds']}s)")
        print(f"  Best accuracy so far: {state.best_accuracy:.1%}")
        print("-" * 60)

    print(f"\nLoop complete! Final best accuracy: {state.best_accuracy:.1%}")
    print(f"Total iterations: {state.iteration}")
    return state
