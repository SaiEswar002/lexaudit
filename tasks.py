from typing import Dict, Any

TASKS = {
    0: {
        "contract_type": "NDA Agreement",
        "task_description": "Review the NDA agreement and identify risky clauses. There are no missing sections, contradictions, and no rewrite needed.",
        "contract_text": """NON-DISCLOSURE AGREEMENT
        1. Confidentiality: The Receiving Party agrees to keep the Disclosing Party's information strictly confidential. This obligation shall survive in perpetuity and has no expiry date (unlimited_confidentiality).
        2. Penalties: In case of breach, the Receiving Party is reliable to unlimited penalties and the Disclosing Party can sue with no cap on damages (unlimited_penalties).
        3. Scope: Confidential information includes their products, business strategies, and absolutely any unrelated third-party info the Disclosing Party decides to add later (overbroad_scope).
        4. Governing Law: This agreement is governed by the laws of the State, but the Disclosing Party reserves the right to change the governing law anytime without notice (changing_governing_law).
        """,
        "expected_risks": [
            "unlimited_confidentiality",
            "unlimited_penalties",
            "overbroad_scope",
            "changing_governing_law"
        ],
        "expected_missing": [],
        "expected_contradictions": [],
        "expected_rewrite_clause": []
    },
    1: {
        "contract_type": "Employment Contract",
        "task_description": "Review the Employment Contract for risky clauses and missing sections.",
        "contract_text": """EMPLOYMENT CONTRACT
        1. Compensation: The Employee will be paid an annual salary. However, the Employer reserves the right to change the salary anytime at their sole discretion (variable_salary).
        2. Working Hours: The Employee is required to have 24/7 availability with unlimited hours (unlimited_hours).
        3. Non-Compete: The Employee agrees to an excessive non-compete clause, spanning 10 years worldwide after termination (excessive_non_compete).
        4. Intellectual Property: The Employer claims overbroad IP ownership, including personal home projects done entirely on Employee's free time (overbroad_ip_ownership).
        5. Termination: The Employer can terminate this contract with no severance and zero notice (no_notice_termination).
        """,
        "expected_risks": [
            "variable_salary",
            "unlimited_hours",
            "excessive_non_compete",
            "overbroad_ip_ownership",
            "no_notice_termination"
        ],
        "expected_missing": [
            "dispute_resolution",
            "benefits_and_leave"
        ],
        "expected_contradictions": [],
        "expected_rewrite_clause": []
    },
    2: {
        "contract_type": "SaaS License Agreement",
        "task_description": "Review the SaaS License Agreement for risks, missing sections, contradictions, and rewrite the zero_liability clause.",
        "contract_text": """SAAS LICENSE AGREEMENT
        1. Data Usage: We reserve the right for user data resale. User data can be sold to third parties without explicit consent (user_data_resale).
        2. Liability: Under no circumstance shall the company owe any money. The zero liability clause means the company owes $0 under any circumstance, no matter the damage (zero_liability).
        3. Termination: Asymmetric termination ensures the user needs to provide 90 days notice, but the company needs 0 days (asymmetric_termination).
        4. Costs: Forced cost bearing requires the user to pay all legal costs for both parties if a dispute arises (forced_cost_bearing).
        
        5. The company will provide 30 days termination notice before closing the service. (termination_notice_contradiction).
        """,
        "expected_risks": [
            "user_data_resale",
            "zero_liability",
            "asymmetric_termination",
            "forced_cost_bearing"
        ],
        "expected_missing": [
            "privacy_policy_reference",
            "refund_policy"
        ],
        "expected_contradictions": [
            "termination_notice_contradiction"
        ],
        "expected_rewrite_clause": [
            "zero_liability"
        ]
    }
}

def get_task(task_id: int) -> Dict[str, Any]:
    if task_id not in TASKS:
        raise ValueError(f"Task ID {task_id} not found.")
    return TASKS[task_id]

def grade_task(task_id: int, env_state: Dict[str, Any]) -> float:
    """
    Grades the task deterministically yielding a score between 0.0 and 1.0.
    Weighted: risks 40%, missing 30%, contradictions 20%, rewrite 10%
    """
    task = get_task(task_id)
    actions = env_state.get("actions_history", [])
    
    # Track successful targets found by action type
    found_risks = set()
    found_missing = set()
    found_contradictions = set()
    found_rewrites = set()
    
    for act in actions:
        if act["reward"] > 0:  # Successfully gained positive reward
            atype = act["action_type"]
            target = act["target"]
            if atype == "flag_risk":
                found_risks.add(target)
            elif atype == "flag_missing":
                found_missing.add(target)
            elif atype == "flag_contradiction":
                found_contradictions.add(target)
            elif atype == "rewrite_clause":
                found_rewrites.add(target)
                
    # Calculate Risk Score (40%)
    risk_score = 0.0
    if task["expected_risks"]:
        risk_score = len(found_risks) / len(task["expected_risks"])
    else:
        risk_score = 1.0
        
    # Calculate Missing Score (30%)
    missing_score = 0.0
    if task["expected_missing"]:
        missing_score = len(found_missing) / len(task["expected_missing"])
    else:
        missing_score = 1.0
        
    # Calculate Contradictions Score (20%)
    contradiction_score = 0.0
    if task["expected_contradictions"]:
        contradiction_score = len(found_contradictions) / len(task["expected_contradictions"])
    else:
        contradiction_score = 1.0
        
    # Calculate Rewrite Score (10%)
    rewrite_score = 0.0
    if task["expected_rewrite_clause"]:
        rewrite_score = len(found_rewrites) / len(task["expected_rewrite_clause"])
    else:
        rewrite_score = 1.0
        
    final_score = (risk_score * 0.4) + (missing_score * 0.3) + (contradiction_score * 0.2) + (rewrite_score * 0.1)
    
    return round(final_score, 4)
