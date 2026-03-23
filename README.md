# EvolutionProof

Self-improving AI agent whose improvement history is cryptographically verified on-chain.

## What it does

EvolutionProof is an agent that improves its own ability to screen other agents for trustworthiness. Each improvement iteration is logged to Filecoin, and its ERC-8004 TrustScore rises as it demonstrably improves.

## Quick Start

```bash
# 1. Setup
cp .env.example .env
# Fill in API keys

# 2. Install dependencies
pip install -r requirements.txt

# 3. Register identity
python scripts/register_identity.py

# 4. Run the agent loop
python scripts/run_agent.py --iterations 100

# 5. Start dashboard
cd dashboard && npm install && npm run dev
```

## Architecture

```
Agent Loop (Python)
    |
    v
[Screen Agents] -> [Evaluate] -> [Log to Filecoin] -> [Update TrustScore] -> [Improve Prompt]
    ^                                                                              |
    |______________________________________________________________________________|
```

## Tech Stack

- **Inference:** Anthropic API (Claude Sonnet)
- **Storage:** Filecoin Onchain Cloud (FOC) mainnet
- **Identity:** ERC-8004 via AgentProof oracle
- **Chain:** Celo mainnet
- **Treasury:** Lido wstETH yield treasury
- **Payments:** ampersend-sdk spend controls
- **Identity:** ENS (evolutionproof.eth)
- **Dashboard:** Next.js + Recharts

## Project Structure

```
agent/       - Core agent loop, screener, improver, evaluator
chain/       - On-chain integrations (ERC-8004, Filecoin, Celo, Lido, ampersend)
contracts/   - Solidity contracts (StETHTreasury)
eval/        - Ground truth dataset and scoring
dashboard/   - Next.js dashboard
scripts/     - Entry points and setup scripts
tests/       - Test suite
```

## Hackathon Context

- Built solo over the weekend of March 21-22 2026 during The Synthesis hackathon
- 3 independent teams integrated AgentProof oracle during the hackathon: Covfefe (trust scoring + GitHub badge), Redemption Arc (trust/risk endpoints + badge), and FloorEscrow/Bogdanoff (counterparty trust checks + feedback loop, partner tier)
- Both EvolutionProof and AgentProof Recruiter GitHub repos carry AgentProof "Powered by" badges
- 110 Filecoin CIDs map 1:1 to agent improvement iterations - the storage IS the proof mechanism, not just a data store
- Celo mainnet treasury contract deployed with 3 verifiable transactions on Celoscan
- ERC-8004 identity registered through AgentProof oracle

## License

MIT
