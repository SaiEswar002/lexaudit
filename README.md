---
title: LexAudit
emoji: ⚖️
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# LexAudit: OpenEnv Legal Contract Auditing

LexAudit is a production-ready OpenEnv environment built for the **Meta x Scaler OpenEnv Hackathon**. An AI agent acts as a legal auditor, reviewing real-world contracts to identify risks, missing sections, contradictions, and rewrite unfair clauses.

## How It Works

The environment follows the standard OpenEnv API (`reset` → `step` → `state`). On each `reset`, the agent receives a contract as its observation. It then takes a sequence of structured actions — flagging risks, missing sections, or contradictions, or rewriting a clause — and receives a reward signal after each step. A final grade (0.0 to 1.0) is computed when the episode ends.
```
reset(task_id) → Observation (contract text + task description)
    ↓
step(action)   → Observation, Reward, Done, State
    ↓
state()        → Full action history + current score
    ↓
grade()        → Final score breakdown (risk / missing / contradiction / rewrite)
```

## Tasks

| Task | Contract Type | Difficulty | What the Agent Must Do |
| :--- | :--- | :--- | :--- |
| 0 | NDA Agreement | Easy | Flag 4 risky clauses |
| 1 | Employment Contract | Medium | Flag 5 risks + 2 missing sections |
| 2 | SaaS License Agreement | Hard | Flag 4 risks + 2 missing + 1 contradiction + rewrite 1 clause |

## Action Space

| `action_type` | Description | Required Parameters |
| :--- | :--- | :--- |
| `flag_risk` | Identify a risky or unfair clause | `target`: risk name |
| `flag_missing` | Detect a missing required section | `target`: section name |
| `flag_contradiction` | Find two contradicting clauses | `target`: contradiction name |
| `rewrite_clause` | Rewrite an unfair clause fairly | `target`: clause name, `content`: rewritten text (>30 chars) |

## Observation Space

| Field | Type | Description |
| :--- | :--- | :--- |
| `contract_text` | str | Full text of the contract |
| `contract_type` | str | Type of contract (NDA, Employment, SaaS) |
| `task_description` | str | Instructions for the current task |
| `steps_remaining` | int | Steps left before episode ends |
| `actions_taken` | list | History of all actions with rewards |

## Reward Function

| Event | Reward |
| :--- | :--- |
| Correct risk flagged | +0.4 |
| Correct missing section found | +0.3 |
| Correct contradiction found | +0.4 |
| Correct rewrite submitted (>30 chars) | +0.5 |
| Wrong target | -0.2 |
| Duplicate action | -0.1 |
| Invalid rewrite (too short) | -0.3 |
| Unknown action type | -0.2 |

## Grading Weights

| Component | Weight | Pass Threshold |
| :--- | :--- | :--- |
| Risk detection | 40% | — |
| Missing sections | 30% | — |
| Contradiction detection | 20% | — |
| Clause rewrite | 10% | — |
| Efficiency bonus | +5% | Solved in < 8 steps |
| **Easy (Task 0)** | | **≥ 0.70** |
| **Medium (Task 1)** | | **≥ 0.50** |
| **Hard (Task 2)** | | **≥ 0.30** |

## API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Health check |
| `POST` | `/reset` | Reset environment, returns observation |
| `POST` | `/step` | Submit an action, returns observation + reward |
| `GET` | `/state` | Current environment state |
| `GET` | `/grade` | Final score breakdown (0.0 to 1.0) |
| `GET` | `/tasks` | List all available tasks |

## Baseline Scores

| Task | Difficulty | Agent | Score |
| :--- | :--- | :--- | :--- |
| 0 | Easy | Heuristic baseline | 1.000 |
| 1 | Medium | Heuristic baseline | 1.000 |
| 2 | Hard | Heuristic baseline | 1.000 |

The heuristic baseline in `inference.py` achieves a perfect score by directly submitting all expected actions. An LLM-based agent using `meta-llama/Llama-3.3-70B-Instruct` is also supported via the HuggingFace Inference Router.

## Setup

### Run Locally
```bash
pip install -r requirements.txt
python app.py
```

### Run with Docker
```bash
docker build -t lexaudit .
docker run -p 7860:7860 lexaudit
```

### Run the Inference Agent
```bash
# Heuristic baseline (no API key needed)
python inference.py

# LLM agent (requires HuggingFace token)
HF_TOKEN=your_token python inference.py
```

## Repository Structure
```
lexaudit/
├── env.py          # LexAuditEnv — reset / step / state
├── tasks.py        # 3 contract tasks with expected answers
├── graders.py      # Scoring logic with weighted breakdown
├── app.py          # FastAPI server (port 7860)
├── gradio_ui.py    # Gradio dashboard (port 7861)
├── inference.py    # Baseline agent (heuristic + LLM)
├── openenv.yaml    # OpenEnv spec
└── Dockerfile      # Production container
```