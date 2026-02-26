#!/usr/bin/env python3
import sys, os, time, json
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.live import Live

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROGRESS_FILE = os.path.join(BASE_DIR, ".warfront_progress.json")
sys.path.insert(0, BASE_DIR)
from ranks import get_rank

# Height fixed to exactly 3 for a 3-line high panel
console = Console(height=3, width=150)

def build_header():
    if not os.path.exists(PROGRESS_FILE): return Text("Loading...")
    try:
        with open(PROGRESS_FILE, "r") as f: prog = json.load(f)
    except: return Text("Error")

    completed = prog.get("completed", [])
    rank = get_rank(len(completed))
    
    # Identified by the latest file in the saves folder
    current_mission = "N/A"
    if os.path.exists(os.path.join(BASE_DIR, "saves")):
        files = [os.path.join(BASE_DIR, "saves", f) for f in os.listdir(os.path.join(BASE_DIR, "saves")) if f.endswith(".py")]
        if files:
            latest_file = max(files, key=os.path.getmtime)
            current_mission = os.path.basename(latest_file).replace(".py", "")

    problems_dir = os.path.join(BASE_DIR, "problems")
    total = len([f for f in os.listdir(problems_dir) if f.endswith(".py")]) if os.path.exists(problems_dir) else 40
    pct = len(completed) / max(total, 1)
    
    header = Text()
    header.append(" ⚔ WARFRONT ", style="bold red")
    header.append(f" | Rank: {rank['icon']} {rank['name']} ", style=f"bold {rank['color']}")
    header.append(f" [{'█'*int(20*pct)}{'░'*int(20*(1-pct))}] {int(pct*100)}% ", style="dim")
    header.append(f" | Operation: {current_mission}", style="bold yellow")
    
    return Panel(header, border_style="bright_black", padding=(0,1))

if __name__ == "__main__":
    console.clear() 
    # Physically block data exceeding 3 lines from leaking to terminal
    with Live(build_header(), console=console, auto_refresh=True, refresh_per_second=1, vertical_overflow="crop") as live:
        while True:
            time.sleep(1)
            live.update(build_header())
