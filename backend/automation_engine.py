import json
from collections import defaultdict
import pyautogui
import time

def analyze_logs(path, hover_threshold=2):
    """
    Load a log JSON file and detect:
      • Mouse “hovers”: same (x,y) repeated > hover_threshold times
      • Repeated key presses: same key pressed > hover_threshold times in a row

    Returns a list of suggestion dicts.
    """
    with open(path, 'r') as f:
        events = json.load(f)

    suggestions = []

    # Detect mouse hovers
    hover_counts = 1
    last_pos = None
    for ev in [e for e in events if e['event']=='mouse_move']:
        pos = (ev['position']['x'], ev['position']['y'])
        if pos == last_pos:
            hover_counts += 1
        else:
            if last_pos and hover_counts >= hover_threshold:
                suggestions.append({
                    'type': 'hover',
                    'position': last_pos,
                    'count': hover_counts,
                    'message': f"Mouse hovered at {last_pos} for {hover_counts} seconds"
                })
            hover_counts = 1
            last_pos = pos
    # final group
    if last_pos and hover_counts >= hover_threshold:
        suggestions.append({
            'type': 'hover',
            'position': last_pos,
            'count': hover_counts,
            'message': f"Mouse hovered at {last_pos} for {hover_counts} seconds"
        })

    # Detect repeated key presses
    key_counts = 1
    last_key = None
    for ev in [e for e in events if e['event']=='key_press']:
        key = ev['key']
        if key == last_key:
            key_counts += 1
        else:
            if last_key and key_counts >= hover_threshold:
                suggestions.append({
                    'type': 'key',
                    'key': last_key,
                    'count': key_counts,
                    'message': f"Key '{last_key}' pressed {key_counts} times"
                })
            key_counts = 1
            last_key = key
    if last_key and key_counts >= hover_threshold:
        suggestions.append({
            'type': 'key',
            'key': last_key,
            'count': key_counts,
            'message': f"Key '{last_key}' pressed {key_counts} times"
        })

    return suggestions



def replay_task(suggestion):
    """
    Given a suggestion dict, perform the corresponding action:
      • hover → click once at the position
      • key → press the key count times
    """
    if suggestion['type'] == 'hover':
        x, y = suggestion['position']
        pyautogui.click(x, y)
    elif suggestion['type'] == 'key':
        key = suggestion['key']
        for _ in range(suggestion['count']):
            pyautogui.press(key)
            time.sleep(0.1)  # slight delay between presses
    else:
        raise ValueError(f"Unknown suggestion type: {suggestion['type']}")
