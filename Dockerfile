FROM python:3.10-slim

# Create a non-root user
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=user . .

EXPOSE 7860
EXPOSE 7861

CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port 7860 & python gradio_ui.py"]
