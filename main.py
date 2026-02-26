#!/usr/bin/env python3
"""WARFRONT — Main Menu (Full ASCII & Paged UX Edition)"""
import os, sys, subprocess, shutil, time, re, json, tty, termios, select
from rich.console import Console, Group
from rich.table import Table
from rich.text import Text
from rich.rule import Rule
from rich.panel import Panel
from rich.live import Live
from rich.align import Align
from rich import box

# ── Configuration ──────────────────────────────────────────
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
PROBLEMS_DIR  = os.path.join(BASE_DIR, "problems")
LAUNCHER_TERM = os.path.join(BASE_DIR, "warfront.sh")
PROGRESS_FILE = os.path.join(BASE_DIR, ".warfront_progress.json")
DONE_SIGNAL   = os.path.join(BASE_DIR, ".warfront_done")
ATTEMPT_SIGNAL = os.path.join(BASE_DIR, ".warfront_attempt")
SAVES_DIR     = os.path.join(BASE_DIR, "saves")
sys.path.insert(0, BASE_DIR)
os.makedirs(SAVES_DIR, exist_ok=True)

from ranks import get_rank, TIER_INFO, TIER_ORDER
console = Console()
WARFRONT_MODE = os.environ.get("WARFRONT_MODE", "terminal")

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE) as f: return json.load(f)
        except: pass
    return {"completed": [], "attempts": {}}

def save_progress(prog):
    with open(PROGRESS_FILE, "w") as f: json.dump(prog, f, indent=2, ensure_ascii=False)

def scan_problems():
    problems = []
    if not os.path.isdir(PROBLEMS_DIR): return []
    for fname in sorted(os.listdir(PROBLEMS_DIR)):
        if not fname.endswith(".py"): continue
        p = {"file":fname, "path":os.path.join(PROBLEMS_DIR, fname), "no":"", "algo":"", "level":"","title":fname, "desc":""}
        try:
            with open(p["path"]) as f:
                for line in f:
                    if not line.startswith("#"): break
                    m = re.match(r"#\s*(\w+):\s*(.+)", line)
                    if m:
                        k, v = m.group(1).strip(), m.group(2).strip()
                        if k == "MISSION":
                            parts = [x.strip() for x in v.split("|")]
                            p["no"], p["algo"], p["level"] = (parts + ["","",""])[:3]
                        elif k in ("TITLE", "DESC"): p[k.lower()] = v
        except: continue
        if p["no"]: problems.append(p)
    for i, pr in enumerate(problems):
        pr["rank"] = get_rank(i); pr["gidx"] = i
    return problems

def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        # 1. Wait for input (timeout None = blocking)
        # 0% CPU usage and instant response
        rlist, _, _ = select.select([sys.stdin], [], [], None)
        
        if rlist:
            key = sys.stdin.read(1)
            # 2. If it starts with Escape(\x1b), read the rest of the sequence
            if key == '\x1b':
                # Check for subsequent characters very briefly
                rlist, _, _ = select.select([sys.stdin], [], [], 0.05)
                if rlist:
                    key += sys.stdin.read(2) # Read [A, [B etc.
            return key
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ""

def build_paged_ui(prog, problems, selected_idx, command_menu=None):
    PAGE_SIZE = 10
    total = len(problems)
    # Ensure selected_idx is within bounds
    selected_idx = max(0, min(selected_idx, total - 1)) if total > 0 else 0
    start_idx = (selected_idx // PAGE_SIZE) * PAGE_SIZE
    end_idx = min(start_idx + PAGE_SIZE, total)
    
    content = []
    # 1. Logo
    logo_art = r"""
  ██╗    ██╗ █████╗ ██████╗ ███████╗███████╗██████╗  ██████╗ ███╗   ██╗████████╗
  ██║    ██║██╔══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗██╔═══██╗████╗  ██║╚══██╔══╝
  ██║ █╗ ██║███████║██████╔╝█████╗  █████╗  ██████╔╝██║   ██║██╔██╗ ██║   ██║
  ██║███╗██║██╔══██║██╔══██╗██╔══╝  ██╔══╝  ██╔══██╗██║   ██║██║╚██╗██║   ██║
  ╚███╔███╔╝██║  ██║██║  ██║██║     ██║     ██║  ██║╚██████╔╝██║ ╚████║   ██║"""
    
    logo = Text(logo_art, style="bold red", no_wrap=True)
    content.append(Align.center(logo))

    # 2. Status Bar
    completed_list = prog.get("completed", [])
    done = len(completed_list)
    mode = "[bold cyan]🌐 WEB[/]" if WARFRONT_MODE=="browser" else "[bold green]🖥️  TERM[/]"
    
    current_rank = get_rank(done)
    pct = done / max(total, 1)
    bar = Text.from_markup(f"  {mode}  Rank: {current_rank['icon']} [bold {current_rank['color']}]{current_rank['name']}[/]  [{'█'*int(25*pct)}{'░'*int(25*(1-pct))}] {done}/{total} ({int(pct*100)}%)")
    content.append(Panel(bar, border_style="bright_black", padding=(0,1)))

    # 3. Table
    table = Table(box=box.SIMPLE, show_lines=False, expand=True, padding=(0,1))
    table.add_column("#", width=3, style="dim")
    table.add_column("Tier", width=12)
    table.add_column("Mission", width=35)
    table.add_column("Stat", width=10, justify="center")
    table.add_column("Description", style="dim")

    if start_idx > 0:
        style = "bold yellow on #21262d" if selected_idx == start_idx - 1 else "dim yellow"
        table.add_row(" <", "", "[ previous missions ]", "", "", style=style)
    else: table.add_row("", "", "", "", "")

    for i in range(start_idx, start_idx + PAGE_SIZE):
        if i < total:
            p = problems[i]
            cursor = "❯" if i == selected_idx else " "
            hilight = "bold white on #21262d" if i == selected_idx else ""
            comp = p["file"] in completed_list
            atts = prog.get("attempts", {}).get(p["file"], 0)
            success_count = "1" if comp else "0"
            rank_info = p["rank"]
            tier_name = TIER_INFO.get(rank_info["group"], (rank_info["group"], "white", "", ""))[0]
            grade_display = f"{rank_info['icon']} {tier_name}"
            table.add_row(f"{cursor}{i+1:>2}", grade_display, f"{'✅' if comp else '▶'} {p['title']}", f"{atts}/{success_count}", p["desc"], style=hilight)
        else: table.add_row("", "", "", "", "")

    if end_idx < total:
        style = "bold yellow on #21262d" if selected_idx == end_idx else "dim yellow"
        table.add_row(" >", "", "[ next missions ]", "", "", style=style)
    else: table.add_row("", "", "", "", "")

    content.append(table)

    # 4. Command Menu (Gemini CLI Style)
    if command_menu:
        menu_items = command_menu["items"]
        menu_selected = command_menu["selected"]
        
        menu_content = Text()
        for idx, (cmd, desc) in enumerate(menu_items):
            pointer = "> " if idx == menu_selected else "  "
            style = "bold cyan" if idx == menu_selected else "dim"
            menu_content.append(f"{pointer}{cmd:<10}", style=style)
            menu_content.append(f"{desc}\n", style="dim")
        
        menu_panel = Panel(
            menu_content, 
            title="[bold blue]Commands[/]", 
            title_align="left",
            border_style="bright_blue", 
            width=45,
            padding=(1, 2)
        )
        content.append(Align.center(menu_panel))
    else:
        content.append(Text(f"\n  Page {(start_idx//PAGE_SIZE)+1} / {(total-1)//PAGE_SIZE + 1}  |  ↑↓ move | Enter start | / commands", style="dim", justify="center"))
    
    return Group(*content)

def show_command_menu():
    menu_items = [
        ("init",   "Reset progress and saves"),
        ("mode",   "Toggle WEB/TERM mode"),
        ("clear",  "Clear terminal screen"),
        ("cancel", "Close menu")
    ]
    selected_idx = 0
    
    while True:
        prog = load_progress(); problems = scan_problems()
        sys.stdout.write("\033[H")
        menu_data = {"items": menu_items, "selected": selected_idx}
        console.print(build_paged_ui(prog, problems, 0, command_menu=menu_data))
        sys.stdout.write("\033[J")
        sys.stdout.flush()
        
        key = get_key()
        if key in ("\x1b[A", "\x1bOA", "k"): selected_idx = (selected_idx - 1) % len(menu_items)
        elif key in ("\x1b[B", "\x1bOB", "j"): selected_idx = (selected_idx + 1) % len(menu_items)
        elif key == "\r":
            cmd = menu_items[selected_idx][0]
            if cmd == "init":
                if os.path.exists(PROGRESS_FILE): os.remove(PROGRESS_FILE)
                if os.path.exists(SAVES_DIR):
                    for f in os.listdir(SAVES_DIR):
                        f_path = os.path.join(SAVES_DIR, f)
                        if os.path.isfile(f_path): os.remove(f_path)
                console.print("\n[bold red]System reset complete. Restarting...[/]")
                time.sleep(1)
                return "init"
            elif cmd == "mode":
                global WARFRONT_MODE
                WARFRONT_MODE = "browser" if WARFRONT_MODE=="terminal" else "terminal"
                with open(os.path.expanduser("~/.warfront_mode"), "w") as f: f.write(WARFRONT_MODE)
                return "mode"
            elif cmd == "clear":
                console.clear()
                return "mode"
            elif cmd == "cancel": return "cancel"
        elif key in ("\x1b", "q", "/"): return "cancel"

def main():
    global WARFRONT_MODE
    selected_idx = 0
    console.clear()
    while True:
        prog = load_progress(); problems = scan_problems()
        if not problems: break
        
        sys.stdout.write("\033[H")
        console.print(build_paged_ui(prog, problems, selected_idx))
        sys.stdout.write("\033[J")
        sys.stdout.flush()
        
        key = get_key()
        if not key: continue
        if key == "q": break
        elif key == "/":
            res = show_command_menu()
            if res == "init":
                selected_idx = 0
                console.clear()
                continue
        elif key == "\r":
            PAGE_SIZE = 10
            total = len(problems)
            start = (selected_idx // PAGE_SIZE) * PAGE_SIZE
            if selected_idx < start or selected_idx >= total: continue
            
            problem = problems[selected_idx]
            # 🎯 [Fix] Clean signal files before entering mission to ensure accurate count
            if os.path.exists(ATTEMPT_SIGNAL): os.remove(ATTEMPT_SIGNAL)
            if os.path.exists(DONE_SIGNAL): os.remove(DONE_SIGNAL)
            
            console.clear()
            if WARFRONT_MODE == "browser":
                save_path = os.path.join(SAVES_DIR, problem["file"])
                if not os.path.exists(save_path): shutil.copy(problem["path"], save_path)
                subprocess.run(["pkill","-f","editor_server.py"], capture_output=True)
                subprocess.Popen([sys.executable, os.path.join(BASE_DIR,"editor_server.py"), "--problem", problem["path"], 
                                "--savefile", save_path, "--mission", problem["no"], "--rank", problem["rank"]["name"]])
                subprocess.run(["tmux","new-window","-t","warfront","-n","CODE"], capture_output=True)
            else:
                subprocess.run(["bash", LAUNCHER_TERM, problem["no"], problem["path"], "none", 
                               problem["rank"]["name"], problem["rank"]["bar_bg"], problem["rank"]["bar_fg"], "1"])
            
            # Wait loop
            while True:
                try:
                    # 🎯 Signal detection for attempts
                    if os.path.exists(ATTEMPT_SIGNAL):
                        os.remove(ATTEMPT_SIGNAL)
                        prog = load_progress()
                        prog.setdefault("attempts", {})[problem["file"]] = prog["attempts"].get(problem["file"], 0) + 1
                        save_progress(prog)

                    # Success signal detection
                    if os.path.exists(DONE_SIGNAL):
                        os.remove(DONE_SIGNAL)
                        prog = load_progress()
                        if problem["file"] not in prog["completed"]: prog["completed"].append(problem["file"])
                        save_progress(prog)
                        break

                    # Check if returned to menu
                    res = subprocess.run(["tmux", "display-message", "-p", "#W"], capture_output=True, text=True)
                    if res.stdout.strip() == "MENU": break
                except: pass
                time.sleep(0.4)
            console.clear()
            
        elif key in ("\x1b[A", "\x1bOA", "k"):
            PAGE_SIZE = 10
            start = (selected_idx // PAGE_SIZE) * PAGE_SIZE
            min_idx = start - (1 if start > 0 else 0)
            if selected_idx > min_idx: selected_idx -= 1
        elif key in ("\x1b[B", "\x1bOB", "j"):
            PAGE_SIZE = 10
            total = len(problems)
            start = (selected_idx // PAGE_SIZE) * PAGE_SIZE
            end = min(start + PAGE_SIZE, total)
            max_idx = end + (1 if end < total else 0) - 1
            if selected_idx < max_idx: selected_idx += 1
        elif key in ("\x1b[D", "\x1bOD", "h"): # 🎯 Left: Page jump previous
            selected_idx = max(0, selected_idx - 10)
        elif key in ("\x1b[C", "\x1bOC", "l"): # 🎯 Right: Page jump next
            total = len(problems)
            selected_idx = min(total - 1, selected_idx + 10)

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
