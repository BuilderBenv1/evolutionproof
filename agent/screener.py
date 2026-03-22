"""Agent screening task logic — classifies agents as trustworthy or not."""

import json
import anthropic
from dotenv import load_dotenv

load_dotenv()

DEFAULT_SCREENING_PROMPT = """You are an AI agent trust screener. Your job is to classify whether an on-chain agent is trustworthy or untrustworthy based on its profile data.

Analyze the following signals:
- tx_count: Number of transactions (higher = more established)
- age_days: How long the agent has been active (older = more established)
- unique_interactions: Number of unique addresses interacted with
- failed_tx_ratio: Ratio of failed transactions (higher = more suspicious)
- erc8004_score: On-chain reputation score 0-100 (higher = better)
- contract_verified: Whether the contract source code is verified
- flagged_interactions: Number of interactions flagged as suspicious
- avg_gas_used: Average gas per transaction (unusually high can indicate complex/malicious operations)
- metadata: Name, category, and description of the agent

Rules for classification:
1. High failed_tx_ratio (>0.15) is a strong negative signal
2. Low age_days (<30) combined with high flagged_interactions is very suspicious
3. Unverified contracts with high gas usage suggest obfuscation
4. High erc8004_score (>50) with long history is a strong positive signal
5. MEV, attack, and spam categories are typically untrustworthy
6. Description text that promises unrealistic returns is suspicious

For each agent, respond with ONLY a JSON object:
{"verdict": "trustworthy"} or {"verdict": "untrustworthy"}
"""


def screen_agents(profiles: list, prompt: str = None, client: anthropic.Anthropic = None) -> dict:
    """Screen a list of agent profiles and return predictions.

    Args:
        profiles: List of agent profile dicts from test_set.json
        prompt: The screening prompt to use (enables self-improvement)
        client: Anthropic client instance

    Returns:
        Dict mapping agent_id -> "trustworthy"|"untrustworthy"
    """
    if prompt is None:
        prompt = DEFAULT_SCREENING_PROMPT
    if client is None:
        client = anthropic.Anthropic()

    predictions = {}

    for profile in profiles:
        agent_id = profile["agent_id"]
        profile_str = json.dumps(profile, indent=2)

        try:
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=100,
                messages=[
                    {
                        "role": "user",
                        "content": f"{prompt}\n\nAgent profile to classify:\n{profile_str}",
                    }
                ],
            )

            result_text = response.content[0].text.strip()
            # Parse the JSON verdict
            try:
                result = json.loads(result_text)
                verdict = result.get("verdict", "untrustworthy")
            except json.JSONDecodeError:
                # Fallback: look for keywords
                lower = result_text.lower()
                if "trustworthy" in lower and "untrustworthy" not in lower:
                    verdict = "trustworthy"
                else:
                    verdict = "untrustworthy"

            predictions[agent_id] = verdict

        except Exception as e:
            print(f"Error screening {agent_id}: {e}")
            predictions[agent_id] = "untrustworthy"  # Conservative default

    return predictions
