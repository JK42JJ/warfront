import os
import json

# Default Configuration
DEFAULT_CONFIG = {
    "animation": {
        "move_speed": 0.2,
        "data_speed": 0.4,
        "ui_refresh_rate": 0.3
    },
    "paths": {
        "log_file": ".warfront_log",
        "done_file": ".warfront_done",
        "progress_file": ".warfront_progress.json"
    },
    "ui": {
        "map_expand": True,
        "show_legend": True,
        "theme": "dark"
    }
}

class Config:
    def __init__(self):
        self.settings = DEFAULT_CONFIG.copy()
        self.config_path = "config.json"
        self.load()

    def load(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    user_config = json.load(f)
                    self._deep_update(self.settings, user_config)
            except Exception as e:
                print(f"Error loading config.json: {e}")

    def _deep_update(self, base_dict, update_dict):
        for k, v in update_dict.items():
            if isinstance(v, dict) and k in base_dict:
                self._deep_update(base_dict[k], v)
            else:
                base_dict[k] = v

    def __getattr__(self, name):
        # Allow direct access to top-level keys
        if name in self.settings:
            return self.settings[name]
        raise AttributeError(f"Config has no attribute '{name}'")

# Singleton instance
cfg = Config()
