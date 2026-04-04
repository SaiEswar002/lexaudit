# app.py
# LexAudit - FastAPI Server

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from env import LexAuditEnv, Action
from tasks import TASKS

app = FastAPI(title="LexAudit Environment API")

# Allow Gradio UI (port 7861) to communicate with FastAPI (port 7860)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Single environment instance
env_instance = LexAuditEnv()

# ─── Request Models ───────────────────────────────────────────────────────────

class ResetRequest(BaseModel):
    task_id: Optional[int] = 0

class StepRequest(BaseModel):
    task_id: int
    action_type: str
    target: str
    content: Optional[str] = None

# ─── Endpoints ────────────────────────────────────────────────────────────────

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "LexAudit Server is running"}

@app.post("/reset")
def reset_env(req: Optional[ResetRequest] = None):
    task_id = req.task_id if req else 0
    if task_id not in TASKS:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    obs = env_instance.reset(task_id)
    return obs.model_dump()

@app.post("/step")
def step_env(req: StepRequest):
    if req.task_id not in TASKS:
        raise HTTPException(status_code=404, detail=f"Task {req.task_id} not found")
    if env_instance.task_id != req.task_id:
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
    return {"error": "Requested task is not the active environment task"}

@app.get("/grade")
def grade(task_id: int = 0):
    from graders import grade_task_detailed
    if env_instance.task_id != task_id:
        return {"error": "Grade requested for inactive task"}
    current_state = env_instance.state()
    steps = current_state.get("current_step", 0)
    result = grade_task_detailed(task_id, current_state, steps)
    return {
        "task_id": task_id,
        "score": result["total_score"],
        "breakdown": result["breakdown"],
        "feedback": result["feedback"],
        "difficulty": result["difficulty"],
        "passed": result["passed"]
    }

@app.get("/tasks")
def list_tasks():
    return [
        {
            "task_id": k,
            "contract_type": v["contract_type"],
            "description": v["task_description"]
        }
        for k, v in TASKS.items()
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=7860, reload=False)