# gradio_ui.py
# LexAudit - Gradio Dashboard UI
# Mounted on FastAPI via gr.mount_gradio_app; both run on port 7860

import gradio as gr
import requests
import json

BASE_URL = "http://localhost:7860"

# ─── Task Metadata ────────────────────────────────────────────────────────────

TASK_INFO = {
    0: {
        "label": "Task 0: NDA Agreement (Easy)",
        "contract_type": "NDA Agreement",
        "difficulty": "🟢 Easy",
        "description": "Review the NDA agreement and identify risky clauses. There are no missing sections, contradictions, and no rewrite needed.",
        "pass_threshold": "70%",
    },
    1: {
        "label": "Task 1: Employment Contract (Medium)",
        "contract_type": "Employment Contract",
        "difficulty": "🟡 Medium",
        "description": "Review the Employment Contract for risky clauses and missing sections.",
        "pass_threshold": "50%",
    },
    2: {
        "label": "Task 2: SaaS License Agreement (Hard)",
        "contract_type": "SaaS License Agreement",
        "difficulty": "🔴 Hard",
        "description": "Review the SaaS License Agreement for risks, missing sections, contradictions, and rewrite the zero_liability clause.",
        "pass_threshold": "30%",
    },
}

ACTION_TYPES = ["flag_risk", "flag_missing", "flag_contradiction", "rewrite_clause"]

# ─── Helper Functions ─────────────────────────────────────────────────────────

def api_get(path: str):
    try:
        resp = requests.get(f"{BASE_URL}{path}", timeout=10)
        resp.raise_for_status()
        return resp.json(), None
    except requests.exceptions.ConnectionError:
        return None, "❌ Cannot connect to FastAPI server. Make sure it's running on port 7860."
    except requests.exceptions.Timeout:
        return None, "❌ Request timed out."
    except Exception as e:
        return None, f"❌ Error: {str(e)}"


def api_post(path: str, payload: dict):
    try:
        resp = requests.post(f"{BASE_URL}{path}", json=payload, timeout=10)
        resp.raise_for_status()
        return resp.json(), None
    except requests.exceptions.ConnectionError:
        return None, "❌ Cannot connect to FastAPI server. Make sure it's running on port 7860."
    except requests.exceptions.Timeout:
        return None, "❌ Request timed out."
    except Exception as e:
        return None, f"❌ Error: {str(e)}"


def make_progress_bar(score: float, color: str = "#6366f1") -> str:
    pct = round(score * 100, 1)
    return f"""
<div style="margin: 6px 0;">
  <div style="display:flex; justify-content:space-between; color:#cbd5e1; font-size:13px; margin-bottom:3px;">
    <span>Progress</span><span>{pct}%</span>
  </div>
  <div style="background:#1e293b; border-radius:6px; height:12px; overflow:hidden;">
    <div style="width:{pct}%; background:linear-gradient(90deg,{color},{color}aa); height:100%; border-radius:6px; transition:width 0.3s;"></div>
  </div>
</div>"""


def score_badge(passed: bool) -> str:
    if passed:
        return '<span style="background:#16a34a; color:#fff; padding:4px 14px; border-radius:20px; font-weight:700; font-size:14px;">✅ PASSED</span>'
    return '<span style="background:#dc2626; color:#fff; padding:4px 14px; border-radius:20px; font-weight:700; font-size:14px;">❌ FAILED</span>'


# ─── Tab 1: Overview ──────────────────────────────────────────────────────────

OVERVIEW_HTML = """
<div style="font-family:'Inter',sans-serif; color:#e2e8f0; padding:10px 0;">

  <div style="background:linear-gradient(135deg,#1e1b4b 0%,#312e81 50%,#1e1b4b 100%);
              border:1px solid #4338ca; border-radius:14px; padding:28px 32px; margin-bottom:24px; text-align:center;">
    <h1 style="font-size:2.2rem; font-weight:800; margin:0 0 10px;
               background:linear-gradient(90deg,#818cf8,#c084fc,#38bdf8); -webkit-background-clip:text;
               -webkit-text-fill-color:transparent;">⚖️ LexAudit</h1>
    <p style="font-size:1.1rem; color:#a5b4fc; margin:0;">Legal Contract Auditing Environment — OpenEnv Hackathon</p>
  </div>

  <div style="background:#1e293b; border:1px solid #334155; border-radius:12px; padding:22px 28px; margin-bottom:22px;">
    <h2 style="color:#818cf8; margin:0 0 12px; font-size:1.1rem;">📋 What is LexAudit?</h2>
    <p style="color:#cbd5e1; line-height:1.7; margin:0;">
      LexAudit is a reinforcement-learning-ready <strong style="color:#c084fc;">OpenEnv environment</strong> where an AI agent
      must audit legal contracts. The agent reads complex, adversarial contract text and takes structured actions to
      <em>flag risks</em>, <em>flag missing clauses</em>, <em>flag contradictions</em>, and <em>rewrite problematic clauses</em>.
      The environment returns step-level rewards and a final graded score based on accuracy and efficiency.
    </p>
  </div>

  <div style="background:#1e293b; border:1px solid #334155; border-radius:12px; padding:22px 28px; margin-bottom:22px;">
    <h2 style="color:#818cf8; margin:0 0 16px; font-size:1.1rem;">🗂️ Available Tasks</h2>
    <table style="width:100%; border-collapse:collapse; color:#cbd5e1; font-size:14px;">
      <thead>
        <tr style="background:#0f172a; color:#94a3b8; text-align:left;">
          <th style="padding:10px 14px; border-radius:6px 0 0 6px;">Task ID</th>
          <th style="padding:10px 14px;">Contract Type</th>
          <th style="padding:10px 14px;">Difficulty</th>
          <th style="padding:10px 14px;">Pass Threshold</th>
          <th style="padding:10px 14px; border-radius:0 6px 6px 0;">Description</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-top:1px solid #1e293b;">
          <td style="padding:12px 14px; color:#6ee7b7; font-weight:700;">0</td>
          <td style="padding:12px 14px;">NDA Agreement</td>
          <td style="padding:12px 14px;">🟢 Easy</td>
          <td style="padding:12px 14px;">70%</td>
          <td style="padding:12px 14px; color:#94a3b8;">Flag 4 risky clauses. No missing, contradictions, or rewrites.</td>
        </tr>
        <tr style="border-top:1px solid #334155;">
          <td style="padding:12px 14px; color:#fde68a; font-weight:700;">1</td>
          <td style="padding:12px 14px;">Employment Contract</td>
          <td style="padding:12px 14px;">🟡 Medium</td>
          <td style="padding:12px 14px;">50%</td>
          <td style="padding:12px 14px; color:#94a3b8;">Flag 5 risks + 2 missing sections.</td>
        </tr>
        <tr style="border-top:1px solid #334155;">
          <td style="padding:12px 14px; color:#fca5a5; font-weight:700;">2</td>
          <td style="padding:12px 14px;">SaaS License Agreement</td>
          <td style="padding:12px 14px;">🔴 Hard</td>
          <td style="padding:12px 14px;">30%</td>
          <td style="padding:12px 14px; color:#94a3b8;">Flag 4 risks, 2 missing, 1 contradiction, rewrite zero_liability.</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div style="background:#1e293b; border:1px solid #334155; border-radius:12px; padding:22px 28px;">
    <h2 style="color:#818cf8; margin:0 0 14px; font-size:1.1rem;">🔌 API Endpoints (FastAPI on :7860)</h2>
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
      <div style="background:#0f172a; border-radius:8px; padding:10px 14px; border:1px solid #1e40af;">
        <code style="color:#38bdf8;">GET /</code><br/><span style="color:#94a3b8; font-size:12px;">Health check</span>
      </div>
      <div style="background:#0f172a; border-radius:8px; padding:10px 14px; border:1px solid #1e40af;">
        <code style="color:#38bdf8;">POST /reset</code><br/><span style="color:#94a3b8; font-size:12px;">Reset environment for a task</span>
      </div>
      <div style="background:#0f172a; border-radius:8px; padding:10px 14px; border:1px solid #1e40af;">
        <code style="color:#38bdf8;">POST /step</code><br/><span style="color:#94a3b8; font-size:12px;">Take an action in the environment</span>
      </div>
      <div style="background:#0f172a; border-radius:8px; padding:10px 14px; border:1px solid #1e40af;">
        <code style="color:#38bdf8;">GET /grade</code><br/><span style="color:#94a3b8; font-size:12px;">Grade current session</span>
      </div>
      <div style="background:#0f172a; border-radius:8px; padding:10px 14px; border:1px solid #1e40af;">
        <code style="color:#38bdf8;">GET /state</code><br/><span style="color:#94a3b8; font-size:12px;">Get current env state</span>
      </div>
      <div style="background:#0f172a; border-radius:8px; padding:10px 14px; border:1px solid #1e40af;">
        <code style="color:#38bdf8;">GET /tasks</code><br/><span style="color:#94a3b8; font-size:12px;">List all tasks</span>
      </div>
    </div>
  </div>
</div>
"""

# ─── Tab 2: Try a Contract ────────────────────────────────────────────────────

def load_contract(task_choice: str):
    task_id = int(task_choice.split(":")[0].strip())
    data, err = api_get(f"/tasks")
    if err:
        # Fallback: load directly from local tasks dict
        try:
            import sys, os
            sys.path.insert(0, os.path.dirname(__file__))
            from tasks import TASKS
            task = TASKS[task_id]
            contract = task["contract_text"]
            desc = task["task_description"]
            info = TASK_INFO[task_id]
            summary = f"""**Contract Type:** {info['contract_type']}  |  **Difficulty:** {info['difficulty']}  |  **Pass Threshold:** {info['pass_threshold']}

**Description:** {desc}"""
            return summary, contract
        except Exception as ex:
            return f"Error: {ex}", ""

    # Try to get full contract from local module (API doesn't expose full text)
    try:
        import sys, os
        sys.path.insert(0, os.path.dirname(__file__))
        from tasks import TASKS
        task = TASKS[task_id]
        contract = task["contract_text"]
        desc = task["task_description"]
        info = TASK_INFO[task_id]
        summary = f"""**Contract Type:** {info['contract_type']}  |  **Difficulty:** {info['difficulty']}  |  **Pass Threshold:** {info['pass_threshold']}

**Description:** {desc}"""
        return summary, contract
    except Exception as ex:
        return f"Error loading contract: {ex}", ""


# ─── Tab 3: Agent Actions ─────────────────────────────────────────────────────

_running_scores = {0: 0.0, 1: 0.0, 2: 0.0}

def reset_environment(task_choice: str):
    task_id = int(task_choice.split(":")[0].strip())
    data, err = api_post("/reset", {"task_id": task_id})
    if err:
        return err, "—"
    _running_scores[task_id] = 0.0
    obs = data
    obs_text = f"""✅ Environment Reset for Task {task_id}

📋 Contract Type  : {obs.get('contract_type', 'N/A')}
📝 Instructions   : {obs.get('instructions', 'N/A')}
📊 Steps Remaining: {obs.get('steps_remaining', 'N/A')}
🔢 Current Step   : {obs.get('current_step', 0)}
"""
    return obs_text, f"Score: 0.00 / 1.00"


def take_action(task_choice: str, action_type: str, target: str, content: str):
    task_id = int(task_choice.split(":")[0].strip())

    if not target or not target.strip():
        return "⚠️ Please enter a Target (clause name) before taking an action.", "—"

    payload = {
        "task_id": task_id,
        "action_type": action_type,
        "target": target.strip(),
        "content": content.strip() if content else None,
    }

    data, err = api_post("/step", payload)
    if err:
        return err, "—"

    obs = data.get("observation", {})
    reward = data.get("reward", {})
    done = data.get("done", False)
    state = data.get("state", {})

    reward_val = reward.get("value", 0.0)
    reason = reward.get("reason", "N/A")
    steps_remaining = obs.get("steps_remaining", "?")
    current_step = obs.get("current_step", "?")

    # Update running score estimate via grade endpoint
    grade_data, _ = api_get(f"/grade?task_id={task_id}")
    if grade_data and "score" in grade_data:
        running_score = grade_data["score"]
    else:
        running_score = _running_scores.get(task_id, 0.0)

    result_text = f"""{'✅' if reward_val > 0 else '❌' if reward_val < 0 else '⚪'} Action: {action_type}  |  Target: {target}

💰 Reward         : {reward_val:+.3f}
💬 Reason         : {reason}
🔢 Step           : {current_step}
📊 Steps Remaining: {steps_remaining}
{'🏁 DONE — Episode Complete!' if done else ''}
"""
    score_display = f"Score: {running_score:.4f} / 1.00  {'✅ Passed!' if grade_data and grade_data.get('passed') else ''}"
    return result_text, score_display


# ─── Tab 4: Live Scores ───────────────────────────────────────────────────────

def get_grade(task_choice: str):
    task_id = int(task_choice.split(":")[0].strip())
    data, err = api_get(f"/grade?task_id={task_id}")

    if err:
        return f"<div style='color:#f87171;padding:20px;'>{err}</div>"

    total = data.get("score", 0.0)
    breakdown = data.get("breakdown", {})
    feedback = data.get("feedback", "No feedback.")
    passed = data.get("passed", False)
    difficulty = data.get("difficulty", "—")
    task_id_resp = data.get("task_id", task_id)

    risk = breakdown.get("risk_score", 0.0)
    missing = breakdown.get("missing_score", 0.0)
    contra = breakdown.get("contradiction_score", 0.0)
    rewrite = breakdown.get("rewrite_score", 0.0)
    bonus = breakdown.get("efficiency_bonus", 0.0)

    # Normalize component bars to their weights for visual clarity
    risk_max = 0.4
    missing_max = 0.3
    contra_max = 0.2
    rewrite_max = 0.1
    bonus_max = 0.05

    def bar(val, max_val, color):
        pct = round((val / max_val) * 100, 1) if max_val > 0 else 0
        return f"""
<div style="margin:10px 0;">
  <div style="display:flex; justify-content:space-between; color:#94a3b8; font-size:12px; margin-bottom:4px;">
    <span>{val:.4f} / {max_val:.2f}</span><span>{pct}%</span>
  </div>
  <div style="background:#0f172a; border-radius:8px; height:14px; overflow:hidden;">
    <div style="width:{pct}%; background:linear-gradient(90deg,{color},{color}bb); height:100%; border-radius:8px; transition:width 0.5s;"></div>
  </div>
</div>"""

    total_pct = round(total * 100, 1)
    ring_color = "#16a34a" if passed else "#dc2626"

    html = f"""
<div style="font-family:'Inter',sans-serif; color:#e2e8f0; padding:8px 0;">

  <div style="display:flex; align-items:center; gap:24px; background:#1e293b;
              border:1px solid #334155; border-radius:14px; padding:24px 28px; margin-bottom:20px;">
    <div style="text-align:center; min-width:110px;">
      <div style="font-size:3rem; font-weight:900; color:{ring_color}; line-height:1;">{total_pct}%</div>
      <div style="color:#64748b; font-size:13px; margin-top:4px;">Total Score</div>
    </div>
    <div style="flex:1;">
      <div style="display:flex; gap:10px; align-items:center; margin-bottom:10px;">
        {score_badge(passed)}
        <span style="background:#1e40af; color:#93c5fd; padding:4px 12px; border-radius:20px;
                      font-size:13px; font-weight:600;">Task {task_id_resp} — {difficulty}</span>
      </div>
      <div style="background:#0f172a; border-radius:8px; height:18px; overflow:hidden; margin-top:8px;">
        <div style="width:{total_pct}%; background:linear-gradient(90deg,#6366f1,#c084fc);
                    height:100%; border-radius:8px; transition:width 0.5s;"></div>
      </div>
    </div>
  </div>

  <div style="background:#1e293b; border:1px solid #334155; border-radius:12px; padding:22px 28px; margin-bottom:18px;">
    <h3 style="color:#818cf8; margin:0 0 16px; font-size:1rem;">📊 Score Breakdown</h3>

    <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px;">

      <div style="background:#0f172a; border-radius:10px; padding:14px 16px; border:1px solid #1e293b;">
        <div style="color:#34d399; font-weight:700; font-size:13px; margin-bottom:4px;">⚡ Risk Score  <span style="color:#64748b; font-weight:400;">(40% weight)</span></div>
        {bar(risk, risk_max, "#34d399")}
      </div>

      <div style="background:#0f172a; border-radius:10px; padding:14px 16px; border:1px solid #1e293b;">
        <div style="color:#38bdf8; font-weight:700; font-size:13px; margin-bottom:4px;">🔍 Missing Score  <span style="color:#64748b; font-weight:400;">(30% weight)</span></div>
        {bar(missing, missing_max, "#38bdf8")}
      </div>

      <div style="background:#0f172a; border-radius:10px; padding:14px 16px; border:1px solid #1e293b;">
        <div style="color:#f59e0b; font-weight:700; font-size:13px; margin-bottom:4px;">⚠️ Contradiction Score  <span style="color:#64748b; font-weight:400;">(20% weight)</span></div>
        {bar(contra, contra_max, "#f59e0b")}
      </div>

      <div style="background:#0f172a; border-radius:10px; padding:14px 16px; border:1px solid #1e293b;">
        <div style="color:#c084fc; font-weight:700; font-size:13px; margin-bottom:4px;">✏️ Rewrite Score  <span style="color:#64748b; font-weight:400;">(10% weight)</span></div>
        {bar(rewrite, rewrite_max, "#c084fc")}
      </div>

    </div>

    <div style="background:#0f172a; border-radius:10px; padding:14px 16px; border:1px solid #1e293b; margin-top:14px;">
      <div style="color:#fde68a; font-weight:700; font-size:13px; margin-bottom:4px;">🚀 Efficiency Bonus  <span style="color:#64748b; font-weight:400;">(up to +5%)</span></div>
      {bar(bonus, bonus_max, "#fde68a")}
    </div>
  </div>

  <div style="background:#1e293b; border:1px solid #334155; border-radius:12px; padding:18px 24px;">
    <h3 style="color:#818cf8; margin:0 0 10px; font-size:1rem;">💬 Feedback</h3>
    <p style="color:#cbd5e1; margin:0; line-height:1.7;">{feedback}</p>
  </div>

</div>"""
    return html


# ─── Tab 5: How It Works ──────────────────────────────────────────────────────

HOW_IT_WORKS_HTML = """
<div style="font-family:'Inter',sans-serif; color:#e2e8f0; padding:10px 0;">

  <div style="background:#1e293b; border:1px solid #334155; border-radius:12px; padding:22px 28px; margin-bottom:20px;">
    <h2 style="color:#818cf8; margin:0 0 12px; font-size:1.1rem;">🧠 Environment Concept</h2>
    <p style="color:#cbd5e1; line-height:1.7; margin:0;">
      LexAudit follows the <strong style="color:#c084fc;">OpenEnv</strong> interface — a lightweight, HTTP-based RL environment
      compatible with any agent framework. Each episode, the agent receives an <em>observation</em> containing the contract text
      and instructions. It then takes sequential <em>actions</em> to audit the contract. The environment returns a <em>reward</em>
      after each step and a detailed <em>grade</em> at the end of the episode.
    </p>
  </div>

  <div style="background:#1e293b; border:1px solid #334155; border-radius:12px; padding:22px 28px; margin-bottom:20px;">
    <h2 style="color:#818cf8; margin:0 0 14px; font-size:1.1rem;">🕹️ Action Space</h2>
    <table style="width:100%; border-collapse:collapse; color:#cbd5e1; font-size:14px;">
      <thead>
        <tr style="background:#0f172a; color:#94a3b8;">
          <th style="padding:10px 14px; text-align:left; border-radius:6px 0 0 6px;">Action Type</th>
          <th style="padding:10px 14px; text-align:left;">Target</th>
          <th style="padding:10px 14px; text-align:left;">Content</th>
          <th style="padding:10px 14px; text-align:left; border-radius:0 6px 6px 0;">When to Use</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-top:1px solid #334155;">
          <td style="padding:10px 14px;"><code style="color:#34d399;">flag_risk</code></td>
          <td style="padding:10px 14px; color:#94a3b8;">clause identifier</td>
          <td style="padding:10px 14px; color:#64748b;">—</td>
          <td style="padding:10px 14px; color:#94a3b8;">Identify a risky/harmful clause</td>
        </tr>
        <tr style="border-top:1px solid #334155;">
          <td style="padding:10px 14px;"><code style="color:#38bdf8;">flag_missing</code></td>
          <td style="padding:10px 14px; color:#94a3b8;">section identifier</td>
          <td style="padding:10px 14px; color:#64748b;">—</td>
          <td style="padding:10px 14px; color:#94a3b8;">Identify a missing section</td>
        </tr>
        <tr style="border-top:1px solid #334155;">
          <td style="padding:10px 14px;"><code style="color:#f59e0b;">flag_contradiction</code></td>
          <td style="padding:10px 14px; color:#94a3b8;">contradiction identifier</td>
          <td style="padding:10px 14px; color:#64748b;">—</td>
          <td style="padding:10px 14px; color:#94a3b8;">Flag contradicting clauses</td>
        </tr>
        <tr style="border-top:1px solid #334155;">
          <td style="padding:10px 14px;"><code style="color:#c084fc;">rewrite_clause</code></td>
          <td style="padding:10px 14px; color:#94a3b8;">clause identifier</td>
          <td style="padding:10px 14px; color:#94a3b8;">rewritten text</td>
          <td style="padding:10px 14px; color:#94a3b8;">Provide improved clause text</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div style="background:#1e293b; border:1px solid #334155; border-radius:12px; padding:22px 28px; margin-bottom:20px;">
    <h2 style="color:#818cf8; margin:0 0 14px; font-size:1.1rem;">👁️ Observation Space</h2>
    <table style="width:100%; border-collapse:collapse; color:#cbd5e1; font-size:14px;">
      <thead>
        <tr style="background:#0f172a; color:#94a3b8;">
          <th style="padding:10px 14px; text-align:left; border-radius:6px 0 0 6px;">Field</th>
          <th style="padding:10px 14px; text-align:left;">Type</th>
          <th style="padding:10px 14px; text-align:left; border-radius:0 6px 6px 0;">Description</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-top:1px solid #334155;">
          <td style="padding:10px 14px;"><code style="color:#38bdf8;">contract_text</code></td>
          <td style="padding:10px 14px; color:#94a3b8;">string</td>
          <td style="padding:10px 14px; color:#94a3b8;">The full contract to audit</td>
        </tr>
        <tr style="border-top:1px solid #334155;">
          <td style="padding:10px 14px;"><code style="color:#38bdf8;">instructions</code></td>
          <td style="padding:10px 14px; color:#94a3b8;">string</td>
          <td style="padding:10px 14px; color:#94a3b8;">Task instructions for the agent</td>
        </tr>
        <tr style="border-top:1px solid #334155;">
          <td style="padding:10px 14px;"><code style="color:#38bdf8;">current_step</code></td>
          <td style="padding:10px 14px; color:#94a3b8;">int</td>
          <td style="padding:10px 14px; color:#94a3b8;">Number of steps taken so far</td>
        </tr>
        <tr style="border-top:1px solid #334155;">
          <td style="padding:10px 14px;"><code style="color:#38bdf8;">steps_remaining</code></td>
          <td style="padding:10px 14px; color:#94a3b8;">int</td>
          <td style="padding:10px 14px; color:#94a3b8;">Steps left before episode ends</td>
        </tr>
        <tr style="border-top:1px solid #334155;">
          <td style="padding:10px 14px;"><code style="color:#38bdf8;">contract_type</code></td>
          <td style="padding:10px 14px; color:#94a3b8;">string</td>
          <td style="padding:10px 14px; color:#94a3b8;">Type of contract (NDA, Employment, SaaS)</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div style="background:#1e293b; border:1px solid #334155; border-radius:12px; padding:22px 28px; margin-bottom:20px;">
    <h2 style="color:#818cf8; margin:0 0 14px; font-size:1.1rem;">💰 Reward Structure</h2>
    <table style="width:100%; border-collapse:collapse; color:#cbd5e1; font-size:14px;">
      <thead>
        <tr style="background:#0f172a; color:#94a3b8;">
          <th style="padding:10px 14px; text-align:left; border-radius:6px 0 0 6px;">Action Result</th>
          <th style="padding:10px 14px; text-align:left;">Reward</th>
          <th style="padding:10px 14px; text-align:left; border-radius:0 6px 6px 0;">Notes</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-top:1px solid #334155;">
          <td style="padding:10px 14px; color:#34d399;">✅ Correct flag/rewrite</td>
          <td style="padding:10px 14px;"><code style="color:#34d399;">+1.0</code></td>
          <td style="padding:10px 14px; color:#94a3b8;">Issue correctly identified</td>
        </tr>
        <tr style="border-top:1px solid #334155;">
          <td style="padding:10px 14px; color:#f87171;">❌ Incorrect flag (false positive)</td>
          <td style="padding:10px 14px;"><code style="color:#f87171;">-0.5</code></td>
          <td style="padding:10px 14px; color:#94a3b8;">Penalized for flagging non-issues</td>
        </tr>
        <tr style="border-top:1px solid #334155;">
          <td style="padding:10px 14px; color:#94a3b8;">⚪ No-op / irrelevant action</td>
          <td style="padding:10px 14px;"><code style="color:#94a3b8;">0.0</code></td>
          <td style="padding:10px 14px; color:#94a3b8;">No reward, no penalty</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div style="background:#1e293b; border:1px solid #334155; border-radius:12px; padding:22px 28px;">
    <h2 style="color:#818cf8; margin:0 0 14px; font-size:1.1rem;">📏 Evaluation Criteria (Final Grade)</h2>
    <table style="width:100%; border-collapse:collapse; color:#cbd5e1; font-size:14px;">
      <thead>
        <tr style="background:#0f172a; color:#94a3b8;">
          <th style="padding:10px 14px; text-align:left; border-radius:6px 0 0 6px;">Component</th>
          <th style="padding:10px 14px; text-align:left;">Weight</th>
          <th style="padding:10px 14px; text-align:left; border-radius:0 6px 6px 0;">Description</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-top:1px solid #334155;">
          <td style="padding:10px 14px; color:#34d399;">Risk Identification</td>
          <td style="padding:10px 14px; font-weight:700;">40%</td>
          <td style="padding:10px 14px; color:#94a3b8;">% of correct risks found, minus false positive penalty</td>
        </tr>
        <tr style="border-top:1px solid #334155;">
          <td style="padding:10px 14px; color:#38bdf8;">Missing Sections</td>
          <td style="padding:10px 14px; font-weight:700;">30%</td>
          <td style="padding:10px 14px; color:#94a3b8;">% of missing sections correctly identified</td>
        </tr>
        <tr style="border-top:1px solid #334155;">
          <td style="padding:10px 14px; color:#f59e0b;">Contradiction Detection</td>
          <td style="padding:10px 14px; font-weight:700;">20%</td>
          <td style="padding:10px 14px; color:#94a3b8;">Binary: found the contradiction or not</td>
        </tr>
        <tr style="border-top:1px solid #334155;">
          <td style="padding:10px 14px; color:#c084fc;">Clause Rewrite</td>
          <td style="padding:10px 14px; font-weight:700;">10%</td>
          <td style="padding:10px 14px; color:#94a3b8;">Quality of rewritten clause (needs &gt;50 chars)</td>
        </tr>
        <tr style="border-top:1px solid #334155;">
          <td style="padding:10px 14px; color:#fde68a;">Efficiency Bonus</td>
          <td style="padding:10px 14px; font-weight:700;">+5%</td>
          <td style="padding:10px 14px; color:#94a3b8;">Bonus for completing in &lt;8 steps (+2% for ≤12 steps)</td>
        </tr>
      </tbody>
    </table>
  </div>

</div>
"""

# ─── Build Gradio App ─────────────────────────────────────────────────────────

TASK_CHOICES = [
    "0: NDA Easy",
    "1: Employment Medium",
    "2: SaaS Hard",
]

css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

* { font-family: 'Inter', sans-serif !important; }

body, .gradio-container {
    background: #0a0f1e !important;
}

.gradio-container {
    max-width: 1100px !important;
    margin: 0 auto !important;
}

.tab-nav button {
    background: #1e293b !important;
    color: #94a3b8 !important;
    border: 1px solid #334155 !important;
    border-radius: 8px 8px 0 0 !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    transition: all 0.2s !important;
}

.tab-nav button.selected {
    background: linear-gradient(135deg, #4338ca, #7c3aed) !important;
    color: #fff !important;
    border-color: #6366f1 !important;
}

.tab-nav button:hover:not(.selected) {
    background: #334155 !important;
    color: #e2e8f0 !important;
}

label, .label-wrap span {
    color: #94a3b8 !important;
    font-weight: 600 !important;
    font-size: 13px !important;
}

input, textarea, select, .input-wrap input, .block {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
}

input:focus, textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 2px rgba(99,102,241,0.2) !important;
}

button.primary {
    background: linear-gradient(135deg, #4338ca, #7c3aed) !important;
    border: none !important;
    color: #fff !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    transition: all 0.2s !important;
}

button.primary:hover {
    background: linear-gradient(135deg, #3730a3, #6d28d9) !important;
    box-shadow: 0 4px 15px rgba(99,102,241,0.4) !important;
    transform: translateY(-1px) !important;
}

button.secondary {
    background: #1e293b !important;
    border: 1px solid #4338ca !important;
    color: #818cf8 !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
}

.gr-form, .form {
    background: transparent !important;
    border: none !important;
}

.panel {
    background: #0f172a !important;
    border: 1px solid #1e293b !important;
    border-radius: 12px !important;
}

footer { display: none !important; }
"""

with gr.Blocks(
    theme=gr.themes.Base(
        primary_hue="indigo",
        secondary_hue="purple",
        neutral_hue="slate",
        font=["Inter", "sans-serif"],
    ),
    css=css,
    title="⚖️ LexAudit — Legal Contract Auditing",
) as demo:

    # ── Header ──────────────────────────────────────────────────────────────
    gr.HTML("""
    <div style="text-align:center; padding:28px 0 12px; font-family:'Inter',sans-serif;">
      <div style="display:inline-flex; align-items:center; gap:12px; background:linear-gradient(135deg,#1e1b4b,#312e81);
                  border:1px solid #4338ca; border-radius:16px; padding:16px 36px; margin-bottom:4px;">
        <span style="font-size:2rem;">⚖️</span>
        <div style="text-align:left;">
          <h1 style="margin:0; font-size:1.8rem; font-weight:900;
                     background:linear-gradient(90deg,#818cf8,#c084fc,#38bdf8);
                     -webkit-background-clip:text; -webkit-text-fill-color:transparent;">LexAudit</h1>
          <p style="margin:0; color:#94a3b8; font-size:0.9rem; font-weight:500;">Legal Contract Auditing Environment · OpenEnv Hackathon</p>
        </div>
      </div>
    </div>
    """)

    with gr.Tabs():

        # ──────────────────────────────────────────────────────────────────
        # TAB 1 — Overview
        # ──────────────────────────────────────────────────────────────────
        with gr.TabItem("🏠 Overview"):
            gr.HTML(OVERVIEW_HTML)

        # ──────────────────────────────────────────────────────────────────
        # TAB 2 — Try a Contract
        # ──────────────────────────────────────────────────────────────────
        with gr.TabItem("📄 Try a Contract"):
            gr.HTML("""
            <div style="color:#818cf8; font-weight:700; font-size:1rem; margin-bottom:6px; padding:4px 0;">
              📄 Browse Contract Text
            </div>
            <p style="color:#64748b; font-size:13px; margin:0 0 14px;">
              Select a task to view the full contract text the agent must audit.
            </p>""")

            with gr.Row():
                contract_task_dd = gr.Dropdown(
                    choices=TASK_CHOICES,
                    value=TASK_CHOICES[0],
                    label="Select Task",
                    interactive=True,
                )
                load_contract_btn = gr.Button("📂 Load Contract", variant="primary")

            contract_summary_md = gr.Markdown(
                value="*Select a task and click Load Contract.*",
                label="Task Summary",
            )
            contract_text_box = gr.Textbox(
                value="",
                label="📃 Contract Text (Read-Only)",
                lines=22,
                interactive=False,
                placeholder="Contract text will appear here after loading...",
            )

            load_contract_btn.click(
                fn=load_contract,
                inputs=[contract_task_dd],
                outputs=[contract_summary_md, contract_text_box],
            )

        # ──────────────────────────────────────────────────────────────────
        # TAB 3 — Agent Actions
        # ──────────────────────────────────────────────────────────────────
        with gr.TabItem("🤖 Agent Actions"):
            gr.HTML("""
            <div style="color:#818cf8; font-weight:700; font-size:1rem; margin-bottom:6px; padding:4px 0;">
              🤖 Interactive Agent Playground
            </div>
            <p style="color:#64748b; font-size:13px; margin:0 0 14px;">
              Reset the environment, then take actions step-by-step to audit the contract.
            </p>""")

            with gr.Row():
                with gr.Column(scale=1):
                    agent_task_dd = gr.Dropdown(
                        choices=TASK_CHOICES,
                        value=TASK_CHOICES[0],
                        label="🗂️ Select Task",
                        interactive=True,
                    )
                    reset_btn = gr.Button("🔄 Reset Environment", variant="secondary")

                    gr.HTML("<hr style='border-color:#1e293b; margin:12px 0;'/>")

                    action_type_dd = gr.Dropdown(
                        choices=ACTION_TYPES,
                        value=ACTION_TYPES[0],
                        label="🕹️ Action Type",
                        interactive=True,
                    )
                    target_tb = gr.Textbox(
                        label="🎯 Target (clause name)",
                        placeholder="e.g. unlimited_confidentiality",
                        lines=1,
                    )
                    content_tb = gr.Textbox(
                        label="📝 Content (for rewrite_clause only)",
                        placeholder="Enter rewritten clause text here...",
                        lines=4,
                    )
                    action_btn = gr.Button("⚡ Take Action", variant="primary")

                with gr.Column(scale=1):
                    obs_output = gr.Textbox(
                        label="📡 Environment Response",
                        lines=14,
                        interactive=False,
                        value="Reset the environment to begin.",
                    )
                    score_label = gr.Textbox(
                        label="📊 Running Score",
                        interactive=False,
                        value="Score: —",
                    )

            reset_btn.click(
                fn=reset_environment,
                inputs=[agent_task_dd],
                outputs=[obs_output, score_label],
            )
            action_btn.click(
                fn=take_action,
                inputs=[agent_task_dd, action_type_dd, target_tb, content_tb],
                outputs=[obs_output, score_label],
            )

        # ──────────────────────────────────────────────────────────────────
        # TAB 4 — Live Scores
        # ──────────────────────────────────────────────────────────────────
        with gr.TabItem("📊 Live Scores"):
            gr.HTML("""
            <div style="color:#818cf8; font-weight:700; font-size:1rem; margin-bottom:6px; padding:4px 0;">
              📊 Grading Dashboard
            </div>
            <p style="color:#64748b; font-size:13px; margin:0 0 14px;">
              After taking actions in the Agent tab, click Get Grade to see your detailed score breakdown.
            </p>""")

            with gr.Row():
                grade_task_dd = gr.Dropdown(
                    choices=TASK_CHOICES,
                    value=TASK_CHOICES[0],
                    label="🗂️ Select Task",
                    interactive=True,
                )
                grade_btn = gr.Button("🏆 Get Grade", variant="primary")

            grade_output_html = gr.HTML(
                value="<div style='color:#64748b; padding:20px; text-align:center;'>Select a task and click Get Grade after taking some actions.</div>"
            )

            grade_btn.click(
                fn=get_grade,
                inputs=[grade_task_dd],
                outputs=[grade_output_html],
            )

        # ──────────────────────────────────────────────────────────────────
        # TAB 5 — How It Works
        # ──────────────────────────────────────────────────────────────────
        with gr.TabItem("📖 How It Works"):
            gr.HTML(HOW_IT_WORKS_HTML)

    # ── Footer ───────────────────────────────────────────────────────────
    gr.HTML("""
    <div style="text-align:center; padding:20px 0 8px; color:#334155; font-size:12px; font-family:'Inter',sans-serif;">
      ⚖️ LexAudit · Built for the Meta × Scaler OpenEnv Hackathon ·
      <span style="color:#4338ca;">FastAPI + Gradio :7860</span>
    </div>
    """)


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
