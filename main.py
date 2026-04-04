# main.py
# LexAudit - Combined FastAPI + Gradio entry point
# Mounts Gradio UI on FastAPI so HuggingFace Space App tab shows the dashboard.

import uvicorn
import gradio as gr
from app import app as fastapi_app
from gradio_ui import demo

# Mount the Gradio demo onto the FastAPI app at root path "/"
# FastAPI API routes (/reset, /step, /grade, /state, /tasks) remain accessible
# because gr.mount_gradio_app adds Gradio at "/" but FastAPI routes take priority.
app = gr.mount_gradio_app(fastapi_app, demo, path="/")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
