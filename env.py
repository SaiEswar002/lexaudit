import copy
from typing import Dict, Any, List, Optional, Tuple
from pydantic import BaseModel, Field

from tasks import get_task
from graders import grade_task

class Observation(BaseModel):
    contract_text: str
    contract_type: str
    task_description: str
    steps_remaining: int
    actions_taken: List[Dict[str, Any]] = Field(default_factory=list)

class Action(BaseModel):
    action_type: str
    target: str
    content: Optional[str] = None

class Reward(BaseModel):
    value: float
    reason: str

class LexAuditEnv:
    def __init__(self):
        self.max_steps = 15
        self.current_step = 0
        self.task_id = 0
        self.task_data = None
        self.actions_history = []
        self._done = False
        
    def reset(self, task_id: int = 0) -> Observation:
        self.task_id = task_id
        self.current_step = 0
        self.task_data = get_task(task_id)
        self.actions_history = []
        self._done = False
        return self._get_observation()
        
    def _get_observation(self) -> Observation:
        return Observation(
            contract_text=self.task_data["contract_text"],
            contract_type=self.task_data["contract_type"],
            task_description=self.task_data["task_description"],
            steps_remaining=self.max_steps - self.current_step,
            actions_taken=copy.deepcopy(self.actions_history)
        )
        
    def step(self, action: Action) -> Tuple[Observation, Reward, bool, Dict[str, Any]]:
        if self._done:
            return self._get_observation(), Reward(value=0.0, reason="Episode is done"), True, self.state()
            
        reward_value = 0.0
        reason = ""
        
        valid_actions = ["flag_risk", "flag_missing", "flag_contradiction", "rewrite_clause"]
        if action.action_type not in valid_actions:
            reward_value = -0.2
            reason = f"Unknown action type: {action.action_type}"
        else:
            is_duplicate = False
            for prev_act in self.actions_history:
                if prev_act["action_type"] == action.action_type and prev_act["target"] == action.target:
                    is_duplicate = True
                    break
                    
            if is_duplicate:
                reward_value = -0.1
                reason = "Duplicate action on the same target"
            else:
                if action.action_type == "flag_risk":
                    if action.target in self.task_data["expected_risks"]:
                        reward_value = 0.4
                        reason = f"Correctly flagged risk: {action.target}"
                    else:
                        reward_value = -0.2
                        reason = f"Wrong target for risk: {action.target}"
                        
                elif action.action_type == "flag_missing":
                    if action.target in self.task_data["expected_missing"]:
                        reward_value = 0.3
                        reason = f"Correctly flagged missing section: {action.target}"
                    else:
                        reward_value = -0.2
                        reason = f"Wrong target for missing section: {action.target}"
                        
                elif action.action_type == "flag_contradiction":
                    if action.target in self.task_data["expected_contradictions"]:
                        reward_value = 0.4
                        reason = f"Correctly flagged contradiction: {action.target}"
                    else:
                        reward_value = -0.2
                        reason = f"Wrong target for contradiction: {action.target}"
                        
                elif action.action_type == "rewrite_clause":
                    # ✅ FIXED: safe None check — avoids crash on Task 0 & Task 1
                    expected_rw = self.task_data.get("expected_rewrite_clause")
                    if expected_rw and action.target == expected_rw:
                        if action.content and len(action.content) > 30:
                            reward_value = 0.5
                            reason = f"Correct rewrite submitted for: {action.target}"
                        else:
                            reward_value = -0.3
                            reason = f"Error in action: Rewrite content must be > 30 chars for {action.target}"
                    else:
                        reward_value = -0.2
                        reason = f"Wrong target for rewrite: {action.target}"
        
        act_dict = action.model_dump()
        act_dict["reward"] = reward_value
        act_dict["reason"] = reason
        self.actions_history.append(act_dict)
        
        self.current_step += 1
        if self.current_step >= self.max_steps:
            self._done = True
            
        reward = Reward(value=reward_value, reason=reason)
        return self._get_observation(), reward, self._done, self.state()
        
    def state(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "current_step": self.current_step,
            "max_steps": self.max_steps,
            "done": self._done,
            "actions_history": copy.deepcopy(self.actions_history)
        }