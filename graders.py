from tasks import get_task

class GraderSystem:
    
    def grade_task(self, task_id: int, env_state: dict, steps_taken: int = 0) -> dict:
        task = get_task(task_id)
        actions = env_state.get("actions_history", [])
        
        found_risks = set()
        found_missing = set()
        found_contradictions = set()
        found_rewrites = []
        
        wrong_risks = 0
        
        expected_risks_set = set(task.get("expected_risks") or [])
        expected_missing_set = set(task.get("expected_missing") or [])
        expected_contradictions_set = set(task.get("expected_contradictions") or [])
        
        expected_rewrites = task.get("expected_rewrite_clause")
        if not expected_rewrites:
            expected_rewrites_set = set()
        elif isinstance(expected_rewrites, str):
            expected_rewrites_set = {expected_rewrites}
        else:
            expected_rewrites_set = set(expected_rewrites)
        
        for act in actions:
            atype = act.get("action_type")
            target = act.get("target")
            content = act.get("content", "")
            
            if atype == "flag_risk":
                if target in expected_risks_set:
                    found_risks.add(target)
                else:
                    wrong_risks += 1
            elif atype == "flag_missing":
                if target in expected_missing_set:
                    found_missing.add(target)
            elif atype == "flag_contradiction":
                if target in expected_contradictions_set:
                    found_contradictions.add(target)
            elif atype == "rewrite_clause":
                if target in expected_rewrites_set:
                    found_rewrites.append(content)

        # 1. RISK SCORE (40% weight)
        if expected_risks_set:
            risk_base = len(found_risks) / len(expected_risks_set)
        else:
            risk_base = 1.0
            
        risk_penalty = min(0.2, 0.05 * wrong_risks)
        risk_score = max(0.0, risk_base - risk_penalty)
        final_risk = risk_score * 0.4
        
        # 2. MISSING SCORE (30% weight)
        if expected_missing_set:
            missing_base = len(found_missing) / len(expected_missing_set)
        else:
            missing_base = 1.0
        final_missing = missing_base * 0.3
        
        # 3. CONTRADICTION SCORE (20% weight)
        if expected_contradictions_set:
            contradiction_base = 1.0 if len(found_contradictions) > 0 else 0.0
        else:
            contradiction_base = 1.0
        final_contradiction = contradiction_base * 0.2
        
        # 4. REWRITE SCORE (10% weight)
        if expected_rewrites_set:
            valid_rewrite = False
            short_rewrite = False
            for r in found_rewrites:
                if r and len(r) > 50:
                    valid_rewrite = True
                elif r:
                    short_rewrite = True
            
            if valid_rewrite:
                rewrite_base = 1.0
            elif short_rewrite:
                rewrite_base = 0.5
            else:
                rewrite_base = 0.0
        else:
            rewrite_base = 1.0
        final_rewrite = rewrite_base * 0.1
        
        # 5. EFFICIENCY BONUS
        if steps_taken < 8:
            bonus = 0.05
        elif steps_taken <= 12:
            bonus = 0.02
        else:
            bonus = 0.0
            
        base_total = final_risk + final_missing + final_contradiction + final_rewrite
        total_score = min(1.0, base_total + bonus)
        
        # 6. PASSED threshold
        if task_id == 0:
            difficulty = "Easy"
            passed = total_score >= 0.7
        elif task_id == 1:
            difficulty = "Medium"
            passed = total_score >= 0.5
        elif task_id == 2:
            difficulty = "Hard"
            passed = total_score >= 0.3
        else:
            difficulty = "Unknown"
            passed = total_score >= 0.5
            
        # 7. FEEDBACK string
        feedback_parts = []
        
        found_items = []
        if found_risks: found_items.append(f"{len(found_risks)}/{len(expected_risks_set)} risks")
        if found_missing: found_items.append(f"{len(found_missing)}/{len(expected_missing_set)} missing sections")
        if found_contradictions: found_items.append(f"{len(found_contradictions)}/{len(expected_contradictions_set)} contradictions")
        if found_rewrites: found_items.append(f"a rewrite")
        
        if found_items:
            feedback_parts.append(f"You correctly found {', '.join(found_items)}.")
        else:
            feedback_parts.append("You did not find any correct issues.")
            
        missed_risks = expected_risks_set - found_risks
        missed_missing = expected_missing_set - found_missing
        missed_contradictions = expected_contradictions_set - found_contradictions
        
        missed_items = []
        if missed_risks: missed_items.append(f"{len(missed_risks)} risks")
        if missed_missing: missed_items.append(f"{len(missed_missing)} missing sections")
        if missed_contradictions: missed_items.append(f"a contradiction")
        
        expected_rewrite = False
        if expected_rewrites_set:
            if not found_rewrites:
                missed_items.append("the required rewrite")
                expected_rewrite = True
            elif not any(r and len(r) > 50 for r in found_rewrites):
                missed_items.append("a long enough rewrite")
                expected_rewrite = True
                
        if missed_items:
            feedback_parts.append(f"You missed {', '.join(missed_items)}.")
            
        if wrong_risks > 0:
            feedback_parts.append(f"Tip: You flagged {wrong_risks} false positives which penalized your score. Be more precise.")
        elif missed_risks:
            feedback_parts.append("Tip: Review the exact wording for hidden, overbroad, or unlimited liability clauses.")
        elif missed_missing:
            feedback_parts.append("Tip: Ensure standard boilerplate sections like dispute resolution or privacy are present.")
        elif expected_rewrite:
            feedback_parts.append("Tip: Provide a comprehensive and legally robust rewrite (> 50 chars) to resolve the problematic clause.")
        elif steps_taken > 8:
            feedback_parts.append("Tip: You can get an efficiency bonus by finding all issues in fewer steps.")
        else:
            feedback_parts.append("Tip: Excellent work! Consider trying a harder challenge.")
            
        feedback_str = " ".join(feedback_parts)
        
        return {
            "total_score": round(total_score, 4),
            "breakdown": {
                "risk_score": round(final_risk, 4),
                "missing_score": round(final_missing, 4),
                "contradiction_score": round(final_contradiction, 4),
                "rewrite_score": round(final_rewrite, 4),
                "efficiency_bonus": bonus
            },
            "feedback": feedback_str,
            "difficulty": difficulty,
            "passed": passed
        }

def grade_task(task_id: int, env_state: dict) -> float:
    """Simple wrapper that returns just the float score"""
    grader = GraderSystem()
    result = grader.grade_task(task_id, env_state)
    return result["total_score"]

def grade_task_detailed(task_id: int, env_state: dict, steps_taken: int = 0) -> dict:
    """Returns full detailed report"""
    grader = GraderSystem()
    return grader.grade_task(task_id, env_state, steps_taken)
