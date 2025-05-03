import pyautogui
from pynput import keyboard
import time, datetime, os, json

class TaskLogger:
    def __init__(self, output_dir='logs'):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.log_file = None
        self.running = False
        self.log = []

    def on_press(self, key):
        try:
            char = key.char
        except:
            char = str(key)
        self.log.append({
            'timestamp': time.time(),
            'event': 'key_press',
            'key': char
        })

    def start_logging(self):
        # If already running, do nothing
        if self.running:
            print("[TaskLogger] 🔄 Already running")
            return

        # Reset for a fresh session
        self.log = []
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.log_file = os.path.join(self.output_dir, f"tasklog_{timestamp}.json")
        
        # Create a new listener each time
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.running = True

        print(f"[TaskLogger] ▶️ Logging started, output to {self.log_file}")
        self.listener.start()

        try:
            while self.running:
                x, y = pyautogui.position()
                self.log.append({
                    'timestamp': time.time(),
                    'event': 'mouse_move',
                    'position': {'x': x, 'y': y}
                })
                time.sleep(1)
        except Exception as e:
            # Catch unexpected errors but keep running flag intact
            print(f"[TaskLogger] Error during logging loop: {e}")
        finally:
            # If exit was not triggered by stop_logging, still write file
            if self.running:
                self.stop_logging()

    def stop_logging(self):
        if not self.running:
            print("[TaskLogger] ⚠️ Not running")
            return

        self.running = False
        # Stop the listener thread
        try:
            self.listener.stop()
        except Exception:
            pass

        # Write out the log
        with open(self.log_file, 'w') as f:
            json.dump(self.log, f, indent=2)

        print(f"[TaskLogger] ✅ Logs saved to {self.log_file}")

if __name__ == '__main__':
    TaskLogger().start_logging()
