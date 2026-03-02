"""warfront/config.py — Typed dataclass configuration (replaces v1 dict-based Config)"""
from __future__ import annotations
import json
import os
from dataclasses import dataclass, field

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")


@dataclass
class AnimationConfig:
    move_speed: float = 0.2
    data_speed: float = 0.4
    ui_refresh_rate: float = 0.3


@dataclass
class PathConfig:
    log_file: str = ".warfront_log"
    done_file: str = ".warfront_done"
    progress_file: str = ".warfront_progress.json"
    db_file: str = ".warfront_progress.db"
    saves_dir: str = "saves"
    problems_dir: str = "problems"
    engines_dir: str = "engines"


@dataclass
class UIConfig:
    map_expand: bool = True
    show_legend: bool = True
    theme: str = "dark"
    page_size: int = 10


@dataclass
class Config:
    animation: AnimationConfig = field(default_factory=AnimationConfig)
    paths: PathConfig = field(default_factory=PathConfig)
    ui: UIConfig = field(default_factory=UIConfig)

    @classmethod
    def load(cls, config_path: str = CONFIG_FILE) -> "Config":
        """Load config from JSON file, overlaying defaults."""
        cfg = cls()
        if not os.path.exists(config_path):
            return cfg
        try:
            with open(config_path) as f:
                data = json.load(f)
        except Exception:
            return cfg

        if "animation" in data:
            a = data["animation"]
            if "move_speed" in a:
                cfg.animation.move_speed = float(a["move_speed"])
            if "data_speed" in a:
                cfg.animation.data_speed = float(a["data_speed"])
            if "ui_refresh_rate" in a:
                cfg.animation.ui_refresh_rate = float(a["ui_refresh_rate"])

        if "paths" in data:
            p = data["paths"]
            if "log_file" in p:
                cfg.paths.log_file = p["log_file"]
            if "done_file" in p:
                cfg.paths.done_file = p["done_file"]
            if "progress_file" in p:
                cfg.paths.progress_file = p["progress_file"]
            if "db_file" in p:
                cfg.paths.db_file = p["db_file"]
            if "saves_dir" in p:
                cfg.paths.saves_dir = p["saves_dir"]

        if "ui" in data:
            u = data["ui"]
            if "map_expand" in u:
                cfg.ui.map_expand = bool(u["map_expand"])
            if "show_legend" in u:
                cfg.ui.show_legend = bool(u["show_legend"])
            if "theme" in u:
                cfg.ui.theme = u["theme"]
            if "page_size" in u:
                cfg.ui.page_size = int(u["page_size"])

        return cfg


# Singleton instance — loaded once at import
cfg = Config.load()
