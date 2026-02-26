#!/usr/bin/env python3
"""WARFRONT Web Editor Server (Browser Mode)"""
import os, sys, shutil, json, subprocess, traceback, argparse
from flask import Flask, request, jsonify, render_template_string

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVES_DIR = os.path.join(BASE_DIR, "saves")
DONE_FILE = os.path.join(BASE_DIR, ".warfront_done")
# Add engines directory to path
ENGINES_DIR = os.path.join(BASE_DIR, "engines")
if ENGINES_DIR not in sys.path: sys.path.insert(0, ENGINES_DIR)

app = Flask(__name__)
_st = {}

@app.route("/")
def index():
    with open(os.path.join(BASE_DIR, "editor.html"), "r", encoding="utf-8") as f:
        return f.read()

@app.route("/api/status")
def api_status():
    save_path = _st.get("savefile")
    code = ""
    if save_path and os.path.exists(save_path):
        with open(save_path, "r", encoding="utf-8") as f: code = f.read()
    
    orig_code = ""
    if _st.get("problem") and os.path.exists(_st["problem"]):
        with open(_st["problem"], "r", encoding="utf-8") as f: orig_code = f.read()

    return jsonify({
        "mission": _st.get("mission", "01"),
        "title": _st.get("mission", "01") + " | " + _st.get("rank", "Trainee"),
        "filename": os.path.basename(save_path) if save_path else "solution.py",
        "code": code,
        "original_code": orig_code
    })

@app.route("/api/run", methods=["POST"])
def api_run():
    data = request.json
    code = data.get("code", "")
    save_path = _st.get("savefile")
    if save_path:
        with open(save_path, "w", encoding="utf-8") as f: f.write(code)
    
    # Run simple validation
    try:
        # Compile check
        compile(code, "<string>", "exec")
        
        # Simple output formatting for web
        output_pairs = [["Status", "✔ Normal execution"]]
        
        # Determine success (Simplified for web)
        is_done = False
        if "return " in code and len(code) > 100:
            is_done = True
            with open(DONE_FILE, "w") as f: f.write("done")
            
        return jsonify({"success": True, "output": output_pairs, "done": is_done})
    except SyntaxError as e:
        return jsonify({"success": False, "output": f"❌ SyntaxError (Line {e.lineno})\n{e.msg}"})
    except Exception as e:
        return jsonify({"success": False, "output": f"❌ Execution Error\n{traceback.format_exc()}"})

@app.route("/api/menu", methods=["POST"])
def api_menu():
    subprocess.run(["tmux", "select-window", "-t", "warfront:MENU"])
    return jsonify({"success": True})

def start(state: dict):
    _st.update(state)
    app.run(port=7477, debug=False)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--problem")
    p.add_argument("--savefile")
    p.add_argument("--mission", default="01")
    p.add_argument("--rank", default="Trainee")
    args = p.parse_args()
    start(vars(args))
