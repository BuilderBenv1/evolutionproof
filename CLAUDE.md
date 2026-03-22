# EvolutionProof — Self-Improving Agent with Verifiable On-Chain Reputation

## Claude Code Project Scaffold

## PROJECT OVERVIEW

Build a self-improving AI agent whose improvement history is cryptographically verified on-chain. The agent has a specific task, runs 100+ autonomous improvement iterations, logs every iteration to Filecoin, and its ERC-8004 TrustScore rises as it demonstrably improves.

- **Submission owner:** Kieron (submitting under new project name, not AgentProof)
- **Builder:** Ben (architects and builds)
- **Deadline:** March 22, 2026 at 11:59 PM PST
- **Judging:** March 23-25 (keep everything live)

## Target Bounties (in priority order)

| # | Bounty | Prize |
|---|--------|-------|
| 1 | Protocol Labs — Agents With Receipts (ERC-8004) | $4,000 |
| 2 | Protocol Labs — Let the Agent Cook | $4,000 |
| 3 | Synthesis Open Track | $25,059 |
| 4 | Filecoin — Agentic Storage (RFS-2 + RFS-3) | $2,000 |
| 5 | Virtuals — ERC-8183 Open Build | $2,000 |
| 6 | Celo — Best Agent on Celo | $5,000 |
| 7 | Lido — stETH Agent Treasury | $3,000 |
| 8 | ampersend | $500 |
| 9 | ENS Identity | $600 |
| 10 | Status Network (gasless tx) | $50 minimum, nearly free |

**Revised prize ceiling: $35,000+** (comfortably achievable placing across the above targets)

## AGENT TASK (what it actually does)

The agent's job is to improve its own ability to screen other agents for trustworthiness.

- It receives a set of agent profiles (wallet address, on-chain history, metadata)
- It predicts: trustworthy or not
- It is scored against a ground truth eval set
- It iterates: analyses failures, rewrites its own screening prompt/logic, re-evaluates
- Each iteration: score logged to Filecoin, ERC-8004 TrustScore updated via AgentProof oracle
- After 100+ rounds: demonstrable improvement trajectory, fully on-chain

**Why this task specifically:**

- Eval metric is objective (classification accuracy against ground truth)
- Uses AgentProof oracle natively (it screens agents = it IS the use case)
- Narrative is perfect: an agent that learns to trust, by earning trust itself
- ERC-8183 compatible (trust-gated agent interactions)
- No external counterparties needed — self-contained demo

## TECH STACK

```
Inference:       Direct Anthropic API (Claude claude-sonnet-4-20250514)
Agent Loop:      Python (orchestration script)
Persistence:     Filecoin Onchain Cloud (FOC) mainnet — iteration logs
Identity:        ERC-8004 via AgentProof oracle (oracle.agentproof.sh)
Trust Score:     AgentProof TrustScoreOracle on Base
Deployment:      Celo (primary chain for agent operations)
Yield Treasury:  Lido wstETH — agent operating budget
Payments:        ampersend-sdk — spend controls
ENS:             Agent gets an ENS name
Frontend:        Simple Next.js dashboard showing iteration history + score trajectory
```

## REPOSITORY STRUCTURE

```
evolutionproof/
├── CLAUDE.md                    # This file — instructions for Claude Code
├── README.md                    # Human-readable project overview
├── AGENTS.md                    # REQUIRED: agentic judge instructions
├── agent.json                   # REQUIRED: DevSpot Agent Manifest (Protocol Labs)
├── agent_log.json               # REQUIRED: execution log (auto-generated, committed)
├── .env.example                 # All required env vars (no secrets)
├── .env                         # Secrets (gitignored)
│
├── agent/
│   ├── __init__.py
│   ├── core.py                  # Main agent loop orchestrator
│   ├── screener.py              # Agent screening task logic
│   ├── improver.py              # Self-improvement logic (prompt rewriting)
│   ├── evaluator.py             # Eval metric computation
│   └── memory.py               # State management between iterations
│
├── chain/
│   ├── erc8004.py              # ERC-8004 identity registration + reads
│   ├── agentproof.py           # AgentProof oracle calls
│   ├── filecoin.py             # Filecoin FOC storage — log iterations
│   ├── lido.py                 # wstETH yield treasury interactions
│   ├── ampersend.py            # ampersend-sdk spend controls
│   └── celo.py                 # Celo chain interactions
│
├── contracts/
│   ├── StETHTreasury.sol        # Lido bounty: principal-protected yield treasury
│   └── deploy.js               # Hardhat deployment script
│
├── eval/
│   ├── ground_truth.json        # Agent trustworthiness ground truth dataset
│   ├── test_set.json            # Agent profiles for screening task
│   └── scorer.py               # Accuracy computation
│
├── dashboard/
│   ├── package.json
│   ├── pages/
│   │   └── index.js            # Live iteration history + score trajectory
│   └── components/
│       ├── IterationChart.jsx   # Score over time chart
│       └── LogViewer.jsx        # On-chain iteration log viewer
│
├── scripts/
│   ├── run_agent.py            # Entry point: starts improvement loop
│   ├── register_identity.py    # One-time: register ERC-8004 identity
│   ├── setup_treasury.py       # One-time: deploy stETH treasury
│   └── fund_agent.py           # Fund agent with initial yield budget
│
└── tests/
    ├── test_screener.py
    ├── test_evaluator.py
    └── test_chain.py
```

## REQUIRED DELIVERABLES CHECKLIST

### Protocol Labs (both tracks)

- [ ] `agent.json` — DevSpot Agent Manifest
- [ ] `agent_log.json` — structured execution log with decisions, tool calls, retries
- [ ] ERC-8004 identity registered and linked to operator wallet
- [ ] Onchain transactions viewable on block explorer
- [ ] Autonomous decision loop: discover → plan → execute → verify → submit
- [ ] Safety guardrails before irreversible actions
- [ ] Compute budget awareness (track token spend)

### Filecoin (RFS-2 + RFS-3)

- [ ] Deploy against FOC mainnet contracts
- [ ] Every iteration log stored on Filecoin (not IPFS — FOC mainnet)
- [ ] Iteration logs retrievable and verifiable
- [ ] 2-minute demo video showing Filecoin as essential architecture
- [ ] Agent state persists across sessions via Filecoin

### Synthesis Open Track

- [ ] AGENTS.md file in repo root
- [ ] ERC-8004 transfer flow completed via submission skill
- [ ] Project kept live March 23-25 for agentic judging
- [ ] Demo video (strongly recommended)

### Virtuals (ERC-8183)

- [ ] Meaningful ERC-8183 integration
- [ ] Trust-gated agent interactions using ERC-8183 spec

### Celo

- [ ] Agent deployed and operating on Celo
- [ ] Real transactions on Celo mainnet
- [ ] Use stablecoin payments (USDC or cUSD)

### Lido (stETH Treasury)

- [ ] StETHTreasury.sol deployed
- [ ] Principal structurally inaccessible to agent
- [ ] Agent can query and draw from yield balance
- [ ] At least one configurable permission (recipient whitelist recommended)
- [ ] Working on mainnet or L2 (Celo has bridged wstETH)

### ampersend

- [ ] ampersend-sdk installed and used as load-bearing component
- [ ] Spend controls configured for agent wallet

### ENS

- [ ] Agent has an ENS name (e.g. evolutionproof.eth)
- [ ] ENS name used in place of hex address throughout UI

### Status Network (free $50)

- [ ] Deploy any contract to Status Network Sepolia Testnet (Chain ID: 1660990954)
- [ ] Execute one gasless transaction
- [ ] Submit — money for free

## IMPLEMENTATION GUIDE

### Phase 1: Identity & Infrastructure Setup (Day 1 morning)

**1. Register ERC-8004 identity**

```python
# scripts/register_identity.py
# Call AgentProof oracle to register agent identity
# Store agent_id, operator_wallet in .env
# Record transaction hash for Protocol Labs deliverable
```

**2. Deploy StETHTreasury contract**

```solidity
// contracts/StETHTreasury.sol
// Uses wstETH on Celo (bridged)
// Principal locked — only yield flows to spendable balance
// Agent queries: getSpendableBalance()
// Agent draws: withdrawYield(amount, recipient)
// Owner sets: recipientWhitelist, perTxCap
```

**3. Get ENS name**

- Register evolutionproof.eth (or similar) via ENS app
- Point to agent operator wallet

**4. Setup Filecoin FOC**

```python
# chain/filecoin.py
# Connect to FOC mainnet
# Create storage deal for iteration logs
# Store/retrieve JSON blobs keyed by iteration number
```

**5. Setup Anthropic API**

```python
# Direct Anthropic API — Claude claude-sonnet-4-20250514
# All inference calls go straight to Anthropic
# No gateway or middleware
```

### Phase 2: Core Agent Loop (Day 1 afternoon — Day 2)

**The improvement loop (agent/core.py)**

```python
def run_improvement_loop(max_iterations=100):
    state = load_state_from_filecoin()  # Resume if interrupted

    for i in range(state.iteration, max_iterations):
        # 1. EVALUATE current screening logic
        accuracy = evaluator.score(state.current_prompt, eval_set)

        # 2. LOG to Filecoin
        log_entry = {
            "iteration": i,
            "accuracy": accuracy,
            "prompt_hash": hash(state.current_prompt),
            "timestamp": now(),
            "tx_hash": None  # filled after chain write
        }
        filecoin_cid = filecoin.store(log_entry)

        # 3. UPDATE ERC-8004 TrustScore via AgentProof
        tx = agentproof.submit_performance(accuracy, filecoin_cid)
        log_entry["tx_hash"] = tx.hash

        # 4. ANALYSE failures
        failures = evaluator.get_failures(state.current_prompt, eval_set)

        # 5. IMPROVE via Anthropic API
        new_prompt = improver.rewrite(
            current_prompt=state.current_prompt,
            failures=failures,
            iteration=i
        )

        # 6. GUARDRAIL: don't apply if worse
        new_accuracy = evaluator.score(new_prompt, eval_set)
        if new_accuracy >= accuracy:
            state.current_prompt = new_prompt

        # 7. PERSIST state to Filecoin
        state.iteration = i + 1
        filecoin.update_state(state)

        # 8. LOG to agent_log.json (Protocol Labs requirement)
        append_to_agent_log(log_entry)

        print(f"Iteration {i}: {accuracy:.3f} → {new_accuracy:.3f}")
```

**The screening task (agent/screener.py)**

```python
# Agent profiles pulled from AgentProof oracle
# Ground truth: manually labelled set of known good/bad agents
# Prompt instructs LLM to classify based on on-chain signals
# Returns: {agent_id: "trustworthy"|"untrustworthy", confidence: float}
```

**The improver (agent/improver.py)**

```python
# Takes: current_prompt, failure_cases, iteration_number
# Calls Anthropic API directly with meta-prompt:
#   "You are improving an agent screening system.
#    These cases were misclassified: {failures}
#    Rewrite the screening prompt to fix these errors
#    while maintaining performance on other cases."
# Returns: new_prompt string
```

### Phase 3: Smart Contracts (Day 2)

**StETHTreasury.sol — Lido bounty**

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IWstETH {
    function getStETHByWstETH(uint256 wstETHAmount) external view returns (uint256);
    function transfer(address to, uint256 amount) external returns (bool);
}

contract StETHTreasury {
    address public owner;
    address public agent;
    IWstETH public wstETH;

    uint256 public principalDeposited;
    uint256 public lastPrincipalBalance;
    uint256 public perTxCap;
    mapping(address => bool) public recipientWhitelist;

    // Only yield (wstETH appreciation) is spendable
    // Principal is structurally locked

    function getSpendableYield() public view returns (uint256);
    function withdrawYield(uint256 amount, address recipient) external onlyAgent;
    function deposit(uint256 wstETHAmount) external onlyOwner;
    function setRecipientWhitelist(address recipient, bool allowed) external onlyOwner;
    function setPerTxCap(uint256 cap) external onlyOwner;
}
```

### Phase 4: agent.json + AGENTS.md (Day 3 morning)

**agent.json (Protocol Labs DevSpot manifest)**

```json
{
  "name": "EvolutionProof",
  "version": "1.0.0",
  "description": "Self-improving agent trust screener with verifiable on-chain improvement history",
  "operator": "YOUR_OPERATOR_WALLET",
  "erc8004_identity": "YOUR_AGENT_ID",
  "ens_name": "evolutionproof.eth",
  "capabilities": [
    "agent_screening",
    "self_improvement",
    "onchain_logging",
    "reputation_verification"
  ],
  "chains": ["celo", "base", "arbitrum"],
  "endpoints": {
    "screen_agent": "https://evolutionproof.xyz/api/screen",
    "get_score": "https://evolutionproof.xyz/api/score",
    "get_history": "https://evolutionproof.xyz/api/history"
  },
  "tools": [
    "agentproof_oracle",
    "filecoin_storage",
    "anthropic_api",
    "ampersend_payments"
  ]
}
```

**AGENTS.md (Synthesis agentic judge instructions)**

```markdown
# EvolutionProof — Agent Instructions

## What this agent does
EvolutionProof is a self-improving agent trust screener.
It autonomously improves its ability to distinguish trustworthy
from untrustworthy agents, with every improvement logged on-chain.

## How to interact with this agent
curl https://evolutionproof.xyz/api/screen \
  -d '{"agent_address": "0x..."}'

## How to verify improvement history
All iteration logs are stored on Filecoin FOC mainnet.
ERC-8004 TrustScore history: oracle.agentproof.sh/agent/YOUR_AGENT_ID

## ERC-8004 Transfer Flow
[complete per synthesis.md/skill.md instructions]
```

### Phase 5: Dashboard (Day 3 afternoon)

Simple Next.js page showing:

- Current TrustScore (live from AgentProof oracle)
- Accuracy over 100+ iterations (line chart — recharts)
- Last 10 iteration logs with Filecoin CIDs
- Links to all on-chain transactions
- Agent ENS name prominent (never show hex address)

Deploy to Vercel. Keep live through March 25.

### Phase 6: Demo Video (Day 4)

2-minute screen recording showing:

1. Agent loop running (terminal)
2. Filecoin storage call succeeding (FOC explorer)
3. ERC-8004 TrustScore updating (AgentProof oracle)
4. Dashboard showing improvement trajectory
5. stETH yield treasury balance (Lido)
6. Anthropic API inference logs

## ENV VARS REQUIRED

```bash
# Anthropic
ANTHROPIC_API_KEY=

# AgentProof
AGENTPROOF_API_KEY=
AGENTPROOF_AGENT_ID=

# Filecoin FOC
FILECOIN_API_KEY=
FILECOIN_CONTRACT_ADDRESS=

# Chains
CELO_RPC_URL=https://forno.celo.org
BASE_RPC_URL=
OPERATOR_PRIVATE_KEY=    # Agent operator wallet — fund with small amount

# Lido
WSTETH_ADDRESS_CELO=     # Bridged wstETH on Celo
TREASURY_CONTRACT=       # Deployed StETHTreasury address

# ampersend
AMPERSEND_API_KEY=

# ENS
ENS_NAME=evolutionproof.eth

# Status Network (free $50)
STATUS_NETWORK_RPC=https://public.sepolia.rpc.status.im
```

## HANDOVER NOTES FOR KIERON

**What Kieron needs to do:**

1. Create a new GitHub account or org for this project (not linked to AgentProof)
2. Clone this repo into that account
3. Register on Devfolio as a builder for Synthesis
4. Complete the ERC-8004 transfer flow via `curl -s https://synthesis.md/skill.md`
5. Add AGENTS.md to repo root (already scaffolded)
6. Submit via Devfolio before March 22 11:59 PM PST
7. Keep everything live March 23-25 for agentic judging
8. Record 2-minute demo video (Ben can do this or Kieron)
9. Select ALL relevant bounty tracks on submission form:
   - Protocol Labs (both tracks)
   - Filecoin
   - Synthesis Open Track
   - Virtuals ERC-8183
   - Celo
   - Lido
   - ampersend
   - ENS
   - Status Network

**What Ben builds:**

- Everything in this repo
- Deploys contracts
- Runs the agent loop to generate real iteration history
- Hands Kieron a working dashboard URL + GitHub repo

**Project name options:** EvolutionProof, ProofLoop, ChainDarwin, IteraAgent

**Key narrative for submission description:**

> "MiniMax proved today that AI can self-improve. EvolutionProof answers the question nobody asked yet: how do you trust a self-improving agent? Every improvement iteration is logged to Filecoin, verified via ERC-8004, and reflected in an on-chain TrustScore. The agent earns its reputation the same way it earns its operating budget — autonomously."

## BUILD ORDER (4 days)

### Day 1 (Today — March 19)

- [ ] Register ERC-8004 identity (scripts/register_identity.py)
- [ ] Setup Filecoin FOC account + test storage call
- [ ] Setup Anthropic API key + test inference call
- [ ] Build eval set (ground_truth.json — 50 agents, labelled)
- [ ] Build core screener (agent/screener.py)
- [ ] Get agent scoring >50% accuracy baseline

### Day 2 (March 20)

- [ ] Build improvement loop (agent/core.py + agent/improver.py)
- [ ] Run first 20 iterations — confirm improvement happening
- [ ] Deploy StETHTreasury.sol to Celo
- [ ] Wire ampersend-sdk to agent wallet
- [ ] Register ENS name

### Day 3 (March 21)

- [ ] Run full 100+ iteration loop
- [ ] Build dashboard (pages/index.js)
- [ ] Deploy dashboard to Vercel
- [ ] Write agent.json + AGENTS.md
- [ ] Complete Status Network gasless tx
- [ ] Record demo video

### Day 4 (March 22)

- [ ] Final testing — confirm all chain integrations live
- [ ] Kieron submits on Devfolio
- [ ] Select all bounty tracks
- [ ] Submit before 11:59 PM PST

## QUICK START FOR CLAUDE CODE

```bash
# 1. Clone and setup
git clone https://github.com/[kieron-org]/evolutionproof
cd evolutionproof
cp .env.example .env
# Fill in .env vars

# 2. Install dependencies
pip install web3 anthropic requests python-dotenv filecoin-sdk ampersend-sdk

# 3. Register identity
python scripts/register_identity.py

# 4. Run agent loop
python scripts/run_agent.py --iterations 100

# 5. Start dashboard
cd dashboard && npm install && npm run dev
```

## IMPORTANT RULES

- Everything committed to the repo must be built AFTER March 13
- AgentProof is a dependency/tool — not the submission
- agentOS is a dependency/tool — not the submission
- The agent loop, eval set, contracts, dashboard — all new
- Keep dashboard live until at least March 25
- Never submit under AgentProof brand or Ben's name
