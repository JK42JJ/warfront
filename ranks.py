# WARFRONT Rank System — 5 Tiers, 40 Ranks
# Rich color: "yellow", "bright_green", "color(75)", etc.
# tmux color: "colour58" format for terminal bars

RANKS = [
    # ══ Trainee (trainee) 10 Ranks ══════════════════════════════
    ("t01", "Trainee Week 1",   "trainee", "yellow",        "🪖", "colour58",  "colour226"),
    ("t02", "Trainee Week 2",   "trainee", "yellow",        "🪖", "colour58",  "colour226"),
    ("t03", "Trainee Week 3",   "trainee", "yellow",        "🪖", "colour58",  "colour226"),
    ("t04", "Trainee Week 4",   "trainee", "yellow",        "🪖", "colour94",  "colour220"),
    ("t05", "Trainee Week 5",   "trainee", "yellow",        "🪖", "colour94",  "colour220"),
    ("t06", "Trainee Week 6",   "trainee", "bright_yellow", "🪖", "colour94",  "colour220"),
    ("t07", "Trainee Week 7",   "trainee", "bright_yellow", "🪖", "colour100", "colour228"),
    ("t08", "Trainee Week 8",   "trainee", "bright_yellow", "🪖", "colour100", "colour228"),
    ("t09", "Trainee Week 9",   "trainee", "bright_yellow", "🪖", "colour100", "colour228"),
    ("t10", "Ready for Grad",   "trainee", "bright_yellow", "🎽", "colour136", "colour229"),

    # ══ Soldier (soldier) 6 Ranks ═════════════════════════════════
    ("s01", "Private ★",         "soldier", "green",         "⚔",  "colour64",  "colour154"),
    ("s02", "Private FC ★★",     "soldier", "green",         "⚔",  "colour64",  "colour154"),
    ("s03", "Corporal ★★★",     "soldier", "bright_green",  "⚔",  "colour70",  "colour190"),
    ("s04", "Sergeant ★★★★",    "soldier", "bright_green",  "⚔",  "colour70",  "colour190"),
    ("s05", "Master Sergeant",  "soldier", "bright_green",  "⚔",  "colour22",  "colour46" ),
    ("s06", "Honorable Disch",  "soldier", "bright_green",  "🎖", "colour22",  "colour46" ),

    # ══ NCO (nco) 6 Ranks ═══════════════════════════════════
    ("n01", "Staff Sgt ◆",       "nco",     "bright_green",  "🎖", "colour28",  "colour82" ),
    ("n02", "Sgt 1st Class ◆◆",  "nco",     "bright_green",  "🎖", "colour28",  "colour82" ),
    ("n03", "Master Sgt ◆◆◆",    "nco",     "bright_green",  "🎖", "colour34",  "colour118"),
    ("n04", "Sgt Major ◆◆◆◆",   "nco",     "bright_green",  "🎖", "colour34",  "colour118"),
    ("n05", "Warrant Officer ▲",  "nco",     "cyan",          "🎖", "colour30",  "colour51" ),
    ("n06", "Chief Warrant ▲▲",   "nco",     "cyan",          "🌟", "colour30",  "colour51" ),

    # ══ Officer (officer) 6 Ranks ═════════════════════════════════
    ("o01", "2nd Lt ☆",         "officer", "cyan",          "⭐", "colour18",  "colour39" ),
    ("o02", "1st Lt ☆☆",        "officer", "bright_cyan",   "⭐", "colour18",  "colour39" ),
    ("o03", "Captain ☆☆☆",      "officer", "bright_cyan",   "⭐", "colour19",  "colour75" ),
    ("o04", "Major ☆☆☆☆",       "officer", "bright_cyan",   "🌟", "colour19",  "colour75" ),
    ("o05", "Lt Colonel ●",       "officer", "bright_white",  "🌟", "colour54",  "colour183"),
    ("o06", "Colonel ●●",        "officer", "bright_white",  "💫", "colour54",  "colour183"),

    # ══ General (general) 12 Ranks ════════════════════════════════
    ("g01", "Brigadier Gen ★",   "general", "yellow",        "🔱", "colour52",  "colour220"),
    ("g02", "Major Gen ★★",      "general", "yellow",        "🔱", "colour52",  "colour220"),
    ("g03", "Lt General ★★★",    "general", "bright_yellow", "🔱", "colour88",  "colour226"),
    ("g04", "General ★★★★",     "general", "bright_yellow", "🔱", "colour88",  "colour226"),
    ("g05", "Marshal ★5",        "general", "bright_white",  "🔱", "colour130", "colour229"),
    ("g06", "Str Commander",     "general", "bright_white",  "🔱", "colour130", "colour229"),
    ("g07", "Joint Chief",       "general", "bright_white",  "🔱", "colour136", "colour255"),
    ("g08", "Chief of Staff",    "general", "bright_white",  "🔱", "colour136", "colour255"),
    ("g09", "Supreme Cmdr",      "general", "bright_white",  "🏆", "colour94",  "colour255"),
    ("g10", "God of Operations", "general", "bright_white",  "🏆", "colour94",  "colour255"),
    ("g11", "Tactical Legend",   "general", "bright_white",  "🏆", "colour58",  "colour226"),
    ("g12", "LEGEND",            "general", "bright_yellow", "👑", "colour232", "colour226"),
]

_OFFSETS = {"trainee":0,"soldier":10,"nco":16,"officer":22,"general":28}

def get_rank(global_idx: int) -> dict:
    idx = max(0, min(global_idx, len(RANKS)-1))
    rid,name,group,color,icon,bbg,bfg = RANKS[idx]
    return {"id":rid,"name":name,"group":group,"color":color,
            "icon":icon,"bar_bg":bbg,"bar_fg":bfg,"idx":idx}

TIER_INFO = {
    "trainee": ("Trainee", "yellow",       "🪖", "Python Basics"),
    "soldier": ("Soldier", "bright_green", "⚔",  "Algo Intro"),
    "nco":     ("NCO",     "bright_green", "🎖",  "Core Algorithms"),
    "officer": ("Officer", "bright_cyan",  "⭐",  "Advanced Algo"),
    "general": ("General", "bright_yellow","🔱",  "Optimization"),
}
TIER_ORDER = ["trainee","soldier","nco","officer","general"]
