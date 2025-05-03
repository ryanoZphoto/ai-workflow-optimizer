import threading
import os
import tempfile
from fastapi import FastAPI, UploadFile, File
from task_logger import TaskLogger
from automation_engine import analyze_logs
from fastapi import HTTPException
from automation_engine import analyze_logs, replay_task

app = FastAPI()
logger = TaskLogger()

@app.post("/replay")
def replay(index: int):
    """
    Replay a previously analyzed suggestion by its index.
    """
    # Ensure there is a recent log analysis
    if not logger.log_file:
        raise HTTPException(400, "No log file available. Run /stop_and_analyze first.")
    suggestions = analyze_logs(logger.log_file)
    if index < 0 or index >= len(suggestions):
        raise HTTPException(400, f"Index {index} out of range.")
    # Perform the action
    replay_task(suggestions[index])
    return {"status": "replayed", "suggestion": suggestions[index]}


@app.post("/start")
def start_logging():
    if not logger.running:
        thread = threading.Thread(target=logger.start_logging, daemon=True)
        thread.start()
        return {"status": "started"}
    return {"status": "already running"}

@app.post("/stop_and_analyze")
def stop_and_analyze():
    print("[API] stop_and_analyze invoked")        # <— diagnostic log
    logger.stop_logging()
    path = logger.log_file
    suggestions = analyze_logs(path)
    return {"status": "analyzed", "suggestions": suggestions}


    suggestions = analyze_logs(tmp_path)
    os.unlink(tmp_path)
    return {"status": "analyzed", "suggestions": suggestions}
