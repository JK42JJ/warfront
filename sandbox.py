import sys
import os
import importlib
import traceback
import pickle
import io

def run_isolated(solution_path, module_name, data):
    """Use        Run  Result   Output  Return """
    #   Output    
    output_capture = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = output_capture
    
    try:
        with open(solution_path, 'r') as f:
            code = f.read()
        
        import map
        ns = {}
        exec_globals = {
            "__builtins__": __builtins__,
            "deque": __import__("collections").deque,
            "heapq": __import__("heapq"),
            "defaultdict": __import__("collections").defaultdict,
            "math": __import__("math"),
            "itertools": __import__("itertools"),
            "Terrain": map.Terrain,
            "UnitType": map.UnitType,
            "GameMap": map.GameMap,
            "Cell": map.Cell,
        }
        
        exec(compile(code, solution_path, "exec"), exec_globals, ns)
        
        if "solve" not in ns:
            sys.stdout = old_stdout
            return {"status": "error", "message": "❌ solve(data) Function  not found.", "stdout": output_capture.getvalue()}
            
        result = ns["solve"](data)
        
        sys.stdout = old_stdout
        return {"status": "success", "result": result, "stdout": output_capture.getvalue()}

    except Exception:
        sys.stdout = old_stdout
        return {"status": "error", "message": traceback.format_exc(), "stdout": output_capture.getvalue()}

if __name__ == "__main__":
    # watcher.py  pickle Data     
    try:
        input_data = pickle.load(sys.stdin.buffer)
        output = run_isolated(input_data['path'], input_data['mod'], input_data['data'])
        pickle.dump(output, sys.stdout.buffer)
    except Exception as e:
        print(f"Sandbox Critical Error: {e}", file=sys.stderr)
