#!/usr/bin/env python3
"""io_watcher.py — Real-time log optimization and integrity verification"""
import sys, os, time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule

console = Console()

def render_log(content: str, expected_path: str):
    lines = [l for l in content.split("\n") if l.strip()]
    if not lines:
        sys.stdout.write("\033[H\033[2J")
        console.print(Rule("[yellow]📋 I/O / Execution Results[/]"))
        console.print(f"\n  [dim]Log data is empty...[/]")
        return False
    
    header = lines[0]
    sys.stdout.write("\033[H\033[2J")

    # Extract basename to compare filenames
    log_file_basename = os.path.basename(header.replace("FILE:", "").strip()).lower()
    expected_basename = os.path.basename(expected_path).strip().lower()

    if not header.startswith("FILE:") or log_file_basename != expected_basename:
        console.print(Rule("[yellow]📋 I/O / Execution Results[/]"))
        console.print(f"\n  [dim]Waiting for '{expected_basename}'...[/]")
        console.print(f"  [dim](Current Log: {log_file_basename})[/]")
        return False

    body = "\n".join(lines[1:])
    console.print(Rule("[yellow]📋 I/O / Execution Results[/]"))
    
    # Enhanced status determination logic
    is_error = any(kw in body for kw in ["Error", "Error", "❌", "Traceback", "FAILED"])
    is_success = "✔" in header or "✔" in body
    
    if is_error:
        style, title = "red", "❌ Error Occurred"
    elif is_success:
        style, title = "green", "✔ Operation Success"
    else:
        style, title = "yellow", "📡 Waiting for Analysis"
    
    # Limit long logs to last 20 lines
    display_body = body.strip()
    body_lines = display_body.split("\n")
    if len(body_lines) > 25:
        display_body = "... (truncated) ...\n" + "\n".join(body_lines[-20:])

    console.print(Panel(Text(display_body, style="white" if is_error else "bright_green" if is_success else "yellow"), 
                        title=f"[{style}]{title}[/]", 
                        border_style=style, 
                        padding=(1, 1),
                        expand=True))
    return True

def watch(log_path: str, expected_file: str):
    console.clear()
    last_content = ""
    last_success = False
    
    while True:
        try:
            if os.path.exists(log_path):
                content = open(log_path).read()
                #    , Previous  Match  Fail     
                if content != last_content or not last_success:
                    last_success = render_log(content, expected_file)
                    last_content = content
            time.sleep(0.3)
        except KeyboardInterrupt: break

if __name__ == "__main__":
    if len(sys.argv) < 3: sys.exit(1)
    watch(sys.argv[1], sys.argv[2])
