import json
import os

def get_handles():
    if not os.path.exists('handles.txt'): 
        return []
    with open('handles.txt', 'r') as f:
        return [line.strip() for line in f if line.strip()]

def load_cache():
    if not os.path.exists('channel_cache.json'): 
        return {}
    with open('channel_cache.json', 'r') as f:
        return json.load(f)

def save_cache(cache):
    with open('channel_cache.json', 'w') as f:
        json.dump(cache, f, indent=4)

def load_history():
    if not os.path.exists('history.json'): 
        return []
    with open('history.json', 'r') as f:
        return json.load(f)

def save_history(history):
    # Keep the last 50 video IDs to guarantee no repeats on high-upload days
    with open('history.json', 'w') as f:
        json.dump(history[:50], f, indent=4)
