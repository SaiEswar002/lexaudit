from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, Optional
from env import LexAuditEnv, Action
from tasks import TASKS, grade_task

app = FastAPI(title="LexAudit Environment API")

# Store env instances for concurrent users/tasks if needed
# For simplicity in hackathon, we use a single instance
env_instance = LexAuditEnv()

class ResetRequest(BaseModel):
    task_id: int

class StepRequest(BaseModel):
    task_id: int
    action_type: str
    target: str
    content: Optional[str] = None

@app.get("/")
def health_check():
    return {"status": "ok", "message": "LexAudit Server is running"}

@app.post("/reset")
def reset_env(req: ResetRequest):
    if req.task_id not in TASKS:
        raise HTTPException(status_code=404, detail="Task not found")
    obs = env_instance.reset(req.task_id)
    return obs.model_dump()

@app.post("/step")
def step_env(req: StepRequest):
    if env_instance.task_id != req.task_id:
         # Implicit reset if stepping uninitialized or wrong task
         env_instance.reset(req.task_id)
         
    act = Action(
        action_type=req.action_type,
        target=req.target,
        content=req.content
    )
    obs, reward, done, state = env_instance.step(act)
    
    return {
        "observation": obs.model_dump(),
        "reward": reward.model_dump(),
        "done": done,
        "state": state
    }

@app.get("/state")
def get_state(task_id: int = 0):
    if env_instance.task_id == task_id:
        return env_instance.state()
    else:
        # State requested for a task not currently active
        return {"error": "Requested task is not the active environment task"}

@app.get("/grade")
def get_grade(task_id: int = 0):
    if env_instance.task_id == task_id:
        score = grade_task(task_id, env_instance.state())
        return {"task_id": task_id, "score": score}
    else:
        return {"error": "Grade requested for a task that is not currently active"}

@app.get("/tasks")
def list_tasks():
    tasks_summary = []
    for k, v in TASKS.items():
        tasks_summary.append({
            "task_id": k,
            "contract_type": v["contract_type"],
            "description": v["task_description"]
        })
    return tasks_summary
