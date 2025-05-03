# AI Workflow Optimizer

An autonomous RPA assistant that:

1. **Logs** your desktop interactions (mouse moves & key presses).  
2. **Analyzes** those logs to detect repetitive patterns (hovers and repeated keys).  
3. **Replays** selected patterns on command (clicks or key presses) to automate your workflows.

---

## 📂 Project Structure

ai-workflow-optimizer/
├── backend/
│ ├── .venv/ # Python virtual environment
│ ├── logs/ # Generated JSON log files
│ ├── task_logger.py # Captures events
│ ├── automation_engine.py # Detects patterns & replays them
│ ├── main.py # FastAPI endpoints: /start, /stop, /stop_and_analyze, /analyze, /replay
│ └── requirements.txt # Python dependencies
├── frontend/
│ ├── main.js # Electron window bootstrap
│ ├── index.html # UI: Start, Stop & Analyze, and Run buttons
│ ├── package.json # Electron + Axios
│ └── node_modules/ # Installed JS packages
├── docs/ # (Empty) place for design docs
├── .gitignore
└── README.md
---

## ✅ What’s Working

- **Logging**: Click **Start Logging** → your mouse & key events are recorded every second.  
- **Analysis**: Click **Stop & Analyze** → patterns (hovers/key repeats) are detected and listed.  
- **Replay**: Click **Run** next to a suggestion → the tool clicks or presses keys for you.

All endpoints run on `http://127.0.0.1:8000` (FastAPI) and the UI is an Electron app talking to them via Axios.

---

## 🚀 Next Milestones

1. **Persisted Macros**  
   - Save and name accepted patterns for reuse.  
   - Add a “My Macros” list in the UI.

2. **Threshold Controls**  
   - Expose the hover/key threshold in the UI for fine-tuning.  

3. **Scheduling & Hotkeys**  
   - Bind saved macros to hotkeys or cron-style schedules.  

4. **Packaging & Distribution**  
   - Bundle the backend (PyInstaller) and UI (electron-builder) into a single installer.  

5. **Advanced Detection**  
   - Swap in ML-based sequence clustering.  
   - Offer higher-level workflow templates via an LLM.

---

## ⚙️ How to Add This README & Push to Git

1. **Create/Overwrite** `README.md` at the project root. From PowerShell in `C:\ai-workflow-optimizer`:

   ```powershell
   # If you want to paste it manually, open README.md in your editor and paste.
   # Or use a here-string to create it in one go:

   @"
   # AI Workflow Optimizer

   An autonomous RPA assistant that:
   ...
   (paste the full contents from above here)
   ...
   "@ | Out-File -Encoding utf8 README.md
