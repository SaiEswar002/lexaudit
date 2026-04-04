# main.py
# LexAudit - Combined FastAPI + Gradio entry point

import uvicorn
import gradio as gr

# Import FastAPI app and Gradio demo
from app import app as fastapi_app
from gradio_ui import demo

# Mount Gradio UI at root path
# This makes "/" show Gradio dashboard while keeping FastAPI routes accessible
app = gr.mount_gradio_app(fastapi_app, demo, path="/")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
