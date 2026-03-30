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

LexAudit is a robust, production-ready environment designed for the **Meta x Scaler OpenEnv Hackathon**. In this environment, an AI agent acts as a legal auditor reviewing real-world legal contracts like a professional lawyer.

## Environment Concept
The agent reviews 3 types of contracts:
1. NDA Agreement
2. Employment Contract
3. SaaS License Agreement

The agent can identify risks, spot missing sections, highlight contradictions, and even rewrite unfair clauses to be more equitable.

## Action Space
| Action `action_type` | Description | Parameters |
| :--- | :--- | :--- |
| `flag_risk` | Identify risky/unfair clauses | `target`: string (name of the risk) |
| `flag_missing` | Detect missing required sections | `target`: string (name of the section) |
| `flag_contradiction` | Find contradicting clauses | `target`: string (name of contradiction) |
| `rewrite_clause` | Rewrite an unfair clause | `target`: string, `content`: string (>30 chars) |

## Observation Space
| Field | Type | Description |
| :--- | :--- | :--- |
| `contract_text` | str | The full text of the contract. |
| `contract_type` | str | Type of the contract (NDA, etc.). |
| `task_description` | str | Instructions for the current task. |
| `steps_remaining` | int | How many steps are left before termination. |
| `actions_taken` | list | History of all actions with rewards. |

## Reward Function
Rewards are distributed at *every step*:
* Correct risk flagged: **+0.4**
* Correct missing section found: **+0.3**
* Correct contradiction found: **+0.4**
* Correct rewrite submitted (>30 chars): **+0.5**
* Wrong target: **-0.2**
* Duplicate action: **-0.1**
* Error in action: **-0.3**
* Unknown action type: **-0.2**

## Tasks Description
1. **Task 0 (Easy) - NDA**: The agent must find 4 risky clauses such as unlimited confidentiality, but there are no missing sections. No rewrite is needed.
2. **Task 1 (Medium) - Employment**: The agent must spot 5 risks (like variable salary and unlimited hours) and 2 missing sections (dispute resolution, benefits). No rewrite is needed.
3. **Task 2 (Hard) - SaaS**: The agent spots 4 risks, 2 missing sections, 1 contradiction, and must successfully rewrite the `zero_liability` clause.

## API Endpoints
| HTTP Method | Endpoint | Use Case |
| :--- | :--- | :--- |
| `GET` | `/` | Health check |
| `POST` | `/reset` | Resets environment, returns observation |
| `POST` | `/step` | Evaluates an action, returns observation, reward, done |
| `GET` | `/state` | Returns the current environment state |
| `GET` | `/grade` | Calculates and returns the final score (0.0 to 1.0) |
| `GET` | `/tasks` | Lists all available tasks |

## Setup Instructions

### Running Locally with Python
```bash
pip install -r requirements.txt
python app.py
```

### Running with Docker (Production/HuggingFace Spaces)
```bash
docker build -t lexaudit .
docker run -p 7860:7860 lexaudit
```

### Running the Inference Agent
```bash
python inference.py
```

## Baseline Scores
| Task ID | Difficulty | Agent Version | Score |
| :--- | :--- | :--- | :--- |
| 0 | Easy | Baseline Heuristic | 1.0 / 1.0 |
| 1 | Medium | Baseline Heuristic | 1.0 / 1.0 |
| 2 | Hard | Baseline Heuristic | 1.0 / 1.0 |
