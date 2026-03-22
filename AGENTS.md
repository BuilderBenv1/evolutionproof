# EvolutionProof — Agent Instructions

## What this agent does

EvolutionProof is a self-improving agent trust screener. It autonomously improves its ability to distinguish trustworthy from untrustworthy on-chain agents, with every improvement iteration cryptographically logged on Filecoin and verified via ERC-8004.

## How it works

1. The agent receives a set of agent profiles (wallet address, on-chain history, metadata)
2. It predicts whether each agent is trustworthy or untrustworthy
3. It scores itself against a ground truth evaluation set
4. It analyzes its failures and rewrites its own screening logic
5. Each iteration is logged to Filecoin FOC mainnet
6. Its ERC-8004 TrustScore is updated via the AgentProof oracle
7. After 100+ rounds: demonstrable improvement trajectory, fully on-chain

## How to interact with this agent

Screen an agent:
```bash
curl https://evolutionproof.vercel.app/api/screen \
  -H "Content-Type: application/json" \
  -d '{"agent_address": "0x..."}'
```

Get current trust score:
```bash
curl https://evolutionproof.vercel.app/api/score
```

Get improvement history:
```bash
curl https://evolutionproof.vercel.app/api/history
```

## How to verify improvement history

- All iteration logs are stored on Filecoin FOC mainnet
- Each log contains: iteration number, accuracy score, prompt hash, timestamp, tx hash
- ERC-8004 TrustScore history is viewable via AgentProof oracle
- On-chain transactions viewable on Celoscan

## Tech stack

- Inference: Anthropic API (Claude Sonnet)
- Storage: Filecoin Onchain Cloud (FOC) mainnet
- Identity: ERC-8004 via AgentProof oracle
- Chain: Celo mainnet
- Treasury: Lido wstETH yield treasury
- Payments: ampersend-sdk spend controls
- Identity: ENS (evolutionproof.eth)

## Safety guardrails

- Never applies a prompt rewrite that scores worse than the current one
- All decisions logged to Filecoin before execution
- Compute budget tracked per iteration
- Treasury principal structurally inaccessible to the agent
- ampersend spend controls limit per-transaction and daily spend

## ERC-8004 Transfer Flow

The agent's ERC-8004 identity is registered via AgentProof oracle and linked to the operator wallet. Trust score updates are submitted as performance metrics with Filecoin CID evidence.
