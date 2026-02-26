#!/usr/bin/env python3
"""watcher.py — PRD v2.6: Execution counting and data structure normalization"""
import sys, os, time, importlib, traceback, subprocess, pickle
from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

# Set paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path: sys.path.insert(0, BASE_DIR)
# Add engines directory to path for mission modules
ENGINES_DIR = os.path.join(BASE_DIR, "engines")
if ENGINES_DIR not in sys.path: sys.path.insert(0, ENGINES_DIR)

import renderer
import map
from config import cfg

console = Console()
LOG_FILE = os.path.join(BASE_DIR, cfg.paths["log_file"])
DONE_SIGNAL = os.path.join(BASE_DIR, ".warfront_done")
# 🎯 Execution (Save) signal filename
ATTEMPT_SIGNAL = os.path.join(BASE_DIR, ".warfront_attempt")

def write_log(filename, lines):
    with open(LOG_FILE, "w") as f:
        f.write(f"FILE:{os.path.basename(filename)}\n")
        f.write("\n".join(str(l) for l in lines))

def signal_done():
    """Trigger success signal and return to menu"""
    with open(DONE_SIGNAL, "w") as f: f.write("done")
    time.sleep(1)
    subprocess.run(["tmux", "select-window", "-t", "warfront:MENU"], capture_output=True)

def signal_attempt():
    """Trigger execution (save) signal"""
    with open(ATTEMPT_SIGNAL, "w") as f: f.write("attempt")

def build_tactical_view(gmap, solution_path, data_result=None):
    content = []
    if gmap:
        title = os.path.basename(solution_path).replace(".py", "")
        content.append(renderer.build_map_renderable(gmap, title=f"Operation Area: {title}"))
    if data_result:
        content.append(renderer.build_data_panel(data_result, title="Real-time Data Analysis"))
    if cfg.ui["show_legend"]:
        content.append(renderer.build_legend())
    return Group(*content)

def run_simulation_v2(solution_path, module_name):
    try:
        if not os.path.exists(solution_path):
            return None, ["File not found."], "ERROR", None, ""
        user_code = open(solution_path).read()
        
        final_mod = "none"
        for line in user_code.split("\n")[:15]:
            if "MODULE:" in line:
                extracted = line.split("MODULE:")[1].strip()
                if extracted.lower() != "none": final_mod = extracted
                break

        mission_mod = None
        if final_mod != "none":
            try:
                if final_mod in sys.modules: del sys.modules[final_mod]
                mission_mod = importlib.import_module(final_mod)
            except: pass

        if mission_mod and hasattr(mission_mod, "build_map"):
            gmap, start, goal = mission_mod.build_map()
        else:
            gmap = map.GameMap(12, 12); start, goal = (0,0), (11,11)

        data = {"gmap": gmap, "start": start, "goal": goal}
        if mission_mod and hasattr(mission_mod, "get_test_data"):
            try: data.update(mission_mod.get_test_data())
            except: pass

        input_payload = {'path': solution_path, 'mod': final_mod, 'data': data}
        proc = subprocess.Popen([sys.executable, os.path.join(BASE_DIR, "sandbox.py")],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            out, err = proc.communicate(input=pickle.dumps(input_payload), timeout=3)
            if proc.returncode != 0: return gmap, [err.decode()], "ERROR", None, ""
            resp = pickle.loads(out)
            user_stdout = resp.get('stdout', '')
            if resp['status'] == 'error': return gmap, [resp['message']], "ERROR", None, user_stdout
            
            result = resp['result']
            is_empty = not result or (isinstance(result, dict) and not any(result.values()))
            status_msg = "✔ Operation Successful" if not is_empty else "📡 Analyzing Operation..."
            
            logs = [status_msg]
            if user_stdout.strip():
                logs.append("\n[📝 User Output]\n" + user_stdout.strip())
            
            if not is_empty:
                logs.append(f"\n🚀 [RETURN] {result}")
            else:
                logs.append("\n⚠️ No valid result returned yet. (TODO needed)")
            
            steps = None
            if mission_mod and hasattr(mission_mod, "visualize_result"):
                try: steps = mission_mod.visualize_result(gmap, result)
                except: pass
            return gmap, logs, result, steps, user_stdout
        except Exception as e:
            return gmap, [f"Execution Error: {e}"], "ERROR", None, ""
    except Exception as e:
        return None, [f"System Error: {e}"], "ERROR", None, ""

if __name__ == "__main__":
    if len(sys.argv) < 3: sys.exit(1)
    sp, mn, mod, done_flag = sys.argv[2], sys.argv[1], sys.argv[3] if len(sys.argv)>3 else "none", len(sys.argv)>4 and sys.argv[4]=="1"
    
    console.clear()
    last_mtime = 0.0
    last_content = ""
    current_gmap = None
    is_first_run = True
    last_status, last_record = "Waiting", "Waiting for code modifications."
    
    with Live(None, console=console, vertical_overflow="crop") as live:
        while True:
            try:
                if os.path.exists(sp):
                    cur_mtime = os.path.getmtime(sp)
                    if cur_mtime != last_mtime:
                        time.sleep(0.1)
                        
                        # 🎯 [Fix] Verify content change to avoid redundant counts
                        try:
                            with open(sp, "r", encoding="utf-8") as f:
                                cur_content = f.read()
                        except:
                            cur_content = ""

                        # Count attempt only if it's not the first run and content actually changed
                        if not is_first_run and cur_content != last_content:
                            signal_attempt()
                        
                        last_content = cur_content
                        new_gmap, logs, result, steps, _ = run_simulation_v2(sp, mod)
                        write_log(sp, logs)
                        
                        if result == "ERROR":
                            live.update(build_tactical_view(current_gmap or new_gmap, sp))
                        else:
                            if steps and not (is_first_run and done_flag):
                                for step in steps:
                                    current_gmap, last_status, last_record = step[0], step[1], step[2]
                                    live.update(build_tactical_view(current_gmap, sp, {"Status": last_status, "Detail": last_record}))
                                    time.sleep(cfg.animation["move_speed"])
                            
                            if steps: 
                                current_gmap, last_status, last_record = steps[-1][0], steps[-1][1], steps[-1][2]
                            else:
                                current_gmap = new_gmap
                            
                            live.update(build_tactical_view(current_gmap, sp, {"Status": last_status, "Detail": last_record}))
                            
                            if result is not None and not (is_first_run or done_flag):
                                # Success signal only if there is a valid result
                                is_empty = not result or (isinstance(result, dict) and not any(result.values()))
                                if not is_empty:
                                    signal_done()
                        
                        last_mtime = cur_mtime
                        is_first_run = False
                time.sleep(0.2)
            except KeyboardInterrupt: break
            except Exception as e:
                time.sleep(1)
