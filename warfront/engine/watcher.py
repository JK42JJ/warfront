"""warfront/engine/watcher.py — watchdog-based file watcher (replaces os.path.getmtime polling).

Uses watchdog.FileSystemEventHandler with a 150 ms debounce to avoid
multiple events per save. Events are pushed to a queue.Queue consumed
by the main visualization loop.
"""
from __future__ import annotations
import os
import queue
import threading
from typing import Callable, Optional

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileModifiedEvent
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False


class _DebounceHandler:
    """Wrap a callback with a 150 ms debounce timer."""

    def __init__(self, callback: Callable[[], None], delay: float = 0.15) -> None:
        self._callback = callback
        self._delay = delay
        self._timer: Optional[threading.Timer] = None
        self._lock = threading.Lock()

    def trigger(self) -> None:
        with self._lock:
            if self._timer is not None:
                self._timer.cancel()
            self._timer = threading.Timer(self._delay, self._callback)
            self._timer.daemon = True
            self._timer.start()

    def cancel(self) -> None:
        with self._lock:
            if self._timer is not None:
                self._timer.cancel()
                self._timer = None


if WATCHDOG_AVAILABLE:
    class _SolutionEventHandler(FileSystemEventHandler):
        def __init__(self, solution_path: str, debounce: _DebounceHandler) -> None:
            super().__init__()
            self._target = os.path.abspath(solution_path)
            self._debounce = debounce

        def on_modified(self, event: FileModifiedEvent) -> None:
            if not event.is_directory and os.path.abspath(event.src_path) == self._target:
                self._debounce.trigger()

        def on_created(self, event) -> None:
            self.on_modified(event)


class SolutionWatcher:
    """Watch *solution_path* for saves and push events to *event_queue*.

    Falls back to polling if watchdog is not installed.
    """

    def __init__(
        self,
        solution_path: str,
        event_queue: "queue.Queue[str]",
        poll_interval: float = 0.5,
    ) -> None:
        self._path = os.path.abspath(solution_path)
        self._q = event_queue
        self._poll_interval = poll_interval
        self._observer: Optional[Observer] = None
        self._debounce: Optional[_DebounceHandler] = None
        self._poll_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

    def _on_change(self) -> None:
        self._q.put(self._path)

    def start(self) -> None:
        if WATCHDOG_AVAILABLE:
            self._debounce = _DebounceHandler(self._on_change, delay=0.15)
            handler = _SolutionEventHandler(self._path, self._debounce)
            self._observer = Observer()
            self._observer.schedule(handler, path=os.path.dirname(self._path), recursive=False)
            self._observer.start()
        else:
            # Fallback: lightweight poll thread
            self._poll_thread = threading.Thread(
                target=self._poll_loop, daemon=True
            )
            self._poll_thread.start()

    def _poll_loop(self) -> None:
        import time
        try:
            last_mtime = os.path.getmtime(self._path)
        except OSError:
            last_mtime = 0.0
        while not self._stop_event.is_set():
            try:
                mtime = os.path.getmtime(self._path)
                if mtime != last_mtime:
                    last_mtime = mtime
                    self._q.put(self._path)
            except OSError:
                pass
            time.sleep(self._poll_interval)

    def stop(self) -> None:
        self._stop_event.set()
        if self._observer:
            self._observer.stop()
            self._observer.join(timeout=2)
        if self._debounce:
            self._debounce.cancel()
