#!/usr/bin/env python3
"""Generate Baekjoon/solved.ac stats SVGs for README."""

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.dates as mdates
from matplotlib.patches import FancyBboxPatch
import numpy as np
import requests
from scipy.interpolate import make_interp_spline

plt.rcParams.update({
    "font.family":    "monospace",
    "font.monospace": ["JetBrains Mono", "Menlo", "Courier New", "DejaVu Sans Mono"],
})

# ── Paths ──────────────────────────────────────────────────────────────────
HANDLE = "sernn"
REPO_ROOT = Path(__file__).parent.parent
DATA_FILE = REPO_ROOT / "data" / "rating_history.json"
ASSETS_DIR = REPO_ROOT / "assets"
BAEKJOON_DIR = REPO_ROOT / "백준"

ASSETS_DIR.mkdir(exist_ok=True)

CANVAS_W  = 9.6   # shared figure width — keeps all three SVGs at the same scale
CONTENT_L = 0.08  # left content margin (fraction of figure width)
CONTENT_R = 0.98  # right content margin

# ── solved.ac tier metadata ─────────────────────────────────────────────────
_TIER_NAMES = (
    ["Unrated"]
    + [f"{t} {r}" for t in ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Ruby"]
       for r in ["V", "IV", "III", "II", "I"]]
)
TIER_COLOR = {
    "Unrated":  "#888888",
    "Bronze":   "#AD5600",
    "Silver":   "#435F7A",
    "Gold":     "#EC9A00",
    "Platinum": "#27E2A4",
    "Diamond":  "#00B4FC",
    "Ruby":     "#FF0062",
}

def tier_name(tier: int) -> str:
    return _TIER_NAMES[tier] if 0 <= tier < len(_TIER_NAMES) else "Unknown"

def tier_color(tier: int) -> str:
    name = tier_name(tier)
    for key in TIER_COLOR:
        if name.startswith(key):
            return TIER_COLOR[key]
    return "#888888"

# ── Language metadata ───────────────────────────────────────────────────────
EXT_TO_LANG = {
    # already tracked
    "cs": "C#", "py": "Python", "c": "C",
    "cpp": "C++", "java": "Java", "js": "JavaScript",
    # additional
    "kt": "Kotlin", "rb": "Ruby", "swift": "Swift",
    "go": "Go", "rs": "Rust", "ts": "TypeScript",
    "scala": "Scala", "php": "PHP", "hs": "Haskell",
    "lua": "Lua", "pl": "Perl", "r": "R", "sh": "Bash",
}
LANG_COLOR = {
    "C#":         "#9B4F96",
    "Python":     "#3572A5",
    "C":          "#6E6E6E",
    "C++":        "#F34B7D",
    "Java":       "#B07219",
    "JavaScript": "#F1E05A",
    "Kotlin":     "#A97BFF",
    "Ruby":       "#701516",
    "Swift":      "#F05138",
    "Go":         "#00ADD8",
    "Rust":       "#DEA584",
    "TypeScript": "#3178C6",
    "Scala":      "#C22D40",
    "PHP":        "#4F5D95",
    "Haskell":    "#5E5086",
    "Lua":        "#000080",
    "Perl":       "#0298C3",
    "R":          "#198CE7",
    "Bash":       "#89E051",
    "Other":      "#8A8A8A",
}

# ── Colour palette ──────────────────────────────────────────────────────────
C_CARD    = "#F7F3FD"
C_BORDER  = "#C8A8E9"
C_TEXT    = "#6B5A8A"
C_MUTED   = "#9B8BB8"
C_ACCENT  = "#8B5CF6"
C_LIGHT   = "#D8C8EF"
C_GRID    = "#E2D5F5"

TIER_GROUP_BOUNDS = {
    "Bronze":   (1, 5),
    "Silver":   (6, 10),
    "Gold":     (11, 15),
    "Platinum": (16, 20),
    "Diamond":  (21, 25),
    "Ruby":     (26, 30),
}

# ── API helpers ─────────────────────────────────────────────────────────────
_HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (compatible; baekjoon-stats-bot/1.0)",
}

def fetch_user_data() -> dict:
    r = requests.get(
        f"https://solved.ac/api/v3/user/show?handle={HANDLE}",
        headers=_HEADERS,
        timeout=10,
    )
    r.raise_for_status()
    return r.json()

def fetch_problem_stats() -> list:
    r = requests.get(
        f"https://solved.ac/api/v3/user/problem_stats?handle={HANDLE}",
        headers=_HEADERS,
        timeout=10,
    )
    r.raise_for_status()
    return r.json()

# ── Data helpers ────────────────────────────────────────────────────────────
def get_language_counts() -> dict:
    counts: dict[str, int] = {}
    for path in BAEKJOON_DIR.rglob("*"):
        if path.is_file():
            ext = path.suffix.lstrip(".").lower()
            if ext in EXT_TO_LANG:
                lang = EXT_TO_LANG[ext]
                counts[lang] = counts.get(lang, 0) + 1
    return counts

def group_by_tier(problem_stats: list) -> dict:
    groups: dict[str, int] = {}
    for stat in problem_stats:
        lvl = stat["level"]
        for name, (lo, hi) in TIER_GROUP_BOUNDS.items():
            if lo <= lvl <= hi:
                groups[name] = groups.get(name, 0) + stat["solved"]
    return groups

def update_history(user_data: dict) -> list:
    DATA_FILE.parent.mkdir(exist_ok=True)
    history: list = json.loads(DATA_FILE.read_text()) if DATA_FILE.exists() else []
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    history = [h for h in history if h["date"] != today]
    history.append({
        "date":   today,
        "rating": user_data["rating"],
        "rank":   user_data["rank"],
        "solved": user_data["solvedCount"],
    })
    history.sort(key=lambda x: x["date"])
    DATA_FILE.write_text(json.dumps(history, indent=2))
    return history


# ── Card 1: Profile (donut + stats + difficulty) ────────────────────────────
def generate_profile_card(user_data: dict, lang_counts: dict, problem_stats: list):
    fig = plt.figure(figsize=(CANVAS_W, 3.2), facecolor="none")

    ax_d = fig.add_axes([0.04, 0.03, 0.44, 0.94])   # donut (filled)
    ax_i = fig.add_axes([0.50, 0.05, 0.48, 0.90])   # info

    for ax in (ax_d, ax_i):
        ax.set_facecolor("none")
        ax.axis("off")

    # ── Donut chart ──────────────────────────────────────────────────────────
    langs  = sorted(lang_counts.items(), key=lambda x: -x[1])
    sizes  = [s for _, s in langs]
    colors = [LANG_COLOR.get(l, LANG_COLOR["Other"]) for l, _ in langs]

    wedges, _ = ax_d.pie(
        sizes,
        colors=colors,
        startangle=90,
        wedgeprops=dict(width=0.44, edgecolor="white", linewidth=0.8),
        radius=1.0,
    )
    # Set limits AFTER pie() so they aren't overridden
    ax_d.set_xlim(-1.22, 1.22)
    ax_d.set_ylim(-1.22, 1.22)

    # ── Info panel ───────────────────────────────────────────────────────────
    ax_i.set_xlim(0, 1)
    ax_i.set_ylim(0, 1)

    # Handle (bigger)
    ax_i.text(0.04, 0.90, HANDLE,
              fontsize=25, fontweight="bold", color=C_TEXT, va="center")

    # Tier (right-aligned)
    t_color = tier_color(user_data["tier"])
    t_name  = tier_name(user_data["tier"])
    ax_i.text(0.96, 0.76, t_name,
              fontsize=13, fontweight="bold", color=t_color,
              va="center", ha="right")

    # Stats rows
    rows = [
        ("Rating", f"{user_data['rating']:,}"),
        ("Rank",   f"#{user_data['rank']:,}"),
        ("Solved", f"{user_data['solvedCount']}"),
    ]
    for i, (label, value) in enumerate(rows):
        y = 0.58 - i * 0.155
        ax_i.text(0.04, y, label, fontsize=9.6, color=C_MUTED, va="center")
        ax_i.text(0.96, y, value, fontsize=12.6, fontweight="bold",
                  color=C_TEXT, va="center", ha="right")
        if i < len(rows) - 1:
            ax_i.plot([0.04, 0.96], [y - 0.075, y - 0.075],
                      color=C_LIGHT, linewidth=0.8)

    # ── Difficulty stacked bar ────────────────────────────────────────────────
    tier_groups = group_by_tier(problem_stats)
    active = [(t, tier_groups[t])
              for t in ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Ruby"]
              if tier_groups.get(t, 0) > 0]

    if active:
        total_s = sum(v for _, v in active)
        ax_i.text(0.04, 0.120, "Difficulty", fontsize=8.4, color=C_MUTED, va="center")

        bx, by, bh = 0.04, 0.028, 0.072

        # Background track
        ax_i.add_patch(FancyBboxPatch(
            (bx - 0.002, by - 0.004), 0.926, bh + 0.008,
            boxstyle="round,pad=0,rounding_size=0.013",
            facecolor=C_LIGHT, edgecolor="none", alpha=0.40, zorder=1,
        ))

        for t_name_g, count in active:
            bw = (count / total_s) * 0.92
            # Segment with tiny inner gap for separation
            ax_i.add_patch(FancyBboxPatch(
                (bx + 0.0018, by + 0.003), max(bw - 0.0036, 0.005), bh - 0.006,
                boxstyle="round,pad=0,rounding_size=0.009",
                facecolor=TIER_COLOR.get(t_name_g, "#888"),
                edgecolor="none", zorder=2,
            ))
            bx += bw

    plt.savefig(ASSETS_DIR / "profile_card.svg",
                format="svg", bbox_inches=None, pad_inches=0, transparent=True)
    plt.close()
    print("  ✓ profile_card.svg")


# ── Card 2: Language legend (horizontal, auto-wrapping) ─────────────────────
def generate_lang_list(lang_counts: dict):
    langs = sorted(lang_counts.items(), key=lambda x: -x[1])
    total = sum(v for _, v in langs)
    n = len(langs)

    ITEMS_PER_ROW = min(4, n)
    n_rows = max(1, (n + ITEMS_PER_ROW - 1) // ITEMS_PER_ROW)
    col_w  = (CONTENT_R - CONTENT_L) / ITEMS_PER_ROW

    fig_w  = CANVAS_W
    fig_h  = n_rows * 0.70

    # Bar: physical height H, width H/3  →  1:3 vertical ratio
    bar_h_in = 0.35
    bar_h    = bar_h_in / fig_h        # data units (ylim 0–1)
    bar_w    = (bar_h_in / 3.0) / fig_w  # data units (xlim 0–1)

    fig = plt.figure(figsize=(fig_w, fig_h), facecolor="none")
    ax  = fig.add_axes([0.0, 0.0, 1.0, 1.0])
    ax.set_facecolor("none")
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    for idx, (lang, count) in enumerate(langs):
        row = idx // ITEMS_PER_ROW
        col = idx % ITEMS_PER_ROW

        bx = CONTENT_L + col * col_w
        cy = 1.0 - (row + 0.5) / n_rows

        pct        = count / total * 100
        lang_color = LANG_COLOR.get(lang, LANG_COLOR["Other"])

        # Thin vertical colored bar
        ax.add_patch(plt.Rectangle(
            (bx, cy - bar_h / 2), bar_w, bar_h,
            color=lang_color, zorder=5, linewidth=0,
        ))

        # Text: language name + percentage
        tx = bx + bar_w + 0.010
        ax.text(tx, cy + bar_h * 0.28, lang,
                ha="left", va="center", fontsize=11, fontweight="bold",
                color=C_TEXT, zorder=5)
        ax.text(tx, cy - bar_h * 0.28, f"{pct:.1f}%",
                ha="left", va="center", fontsize=9,
                color=C_MUTED, zorder=5)

    plt.savefig(ASSETS_DIR / "lang_list.svg",
                format="svg", bbox_inches=None, pad_inches=0, transparent=True)
    plt.close()
    print("  ✓ lang_list.svg")


# ── Card 3: Rating history graph ─────────────────────────────────────────────
def generate_rating_graph(history: list, user_data: dict):
    fig  = plt.figure(figsize=(CANVAS_W, 5.5), facecolor="none")
    ax   = fig.add_axes([0.08, 0.18, 0.71, 0.68])
    ax_r = fig.add_axes([0.81, 0.05, 0.17, 0.90])

    for a in (ax, ax_r):
        a.set_facecolor("none")

    ax_r.axis("off")
    ax_r.set_xlim(0, 1)
    ax_r.set_ylim(0, 1)

    # ── Right info panel ──
    latest = history[-1] if history else user_data
    ax_r.text(0.05, 0.92, "Rating", fontsize=11, color=C_MUTED)
    ax_r.text(0.05, 0.88, str(latest.get("rating", user_data["rating"])),
              fontsize=26, fontweight="bold", color=C_ACCENT, va="top")
    ax_r.text(0.05, 0.72, "Rank", fontsize=11, color=C_MUTED)
    ax_r.text(0.05, 0.64, f"#{latest.get('rank', user_data['rank']):,}",
              fontsize=14, fontweight="bold", color=C_ACCENT)

    if len(history) >= 2:
        prev  = history[-2]
        delta = latest["rating"] - prev["rating"]
        dc = "#4CAF50" if delta > 0 else "#EF5350" if delta < 0 else C_MUTED
        ds = f"▲ +{delta}" if delta > 0 else f"▼ {delta}" if delta < 0 else "─ 0"
        ax_r.text(0.05, 0.58, ds, fontsize=11, color=dc, fontweight="bold")

    # ── Line graph ──
    if len(history) >= 2:
        GRAPH_DAYS = 30
        latest_dt    = datetime.strptime(history[-1]["date"], "%Y-%m-%d")
        first_dt     = datetime.strptime(history[0]["date"], "%Y-%m-%d")
        window_start = max(first_dt, latest_dt - timedelta(days=GRAPH_DAYS - 1))
        window_days  = (latest_dt - window_start).days + 1

        # Forward-fill: missing dates inherit previous day's rating
        hist_dict = {h["date"]: h["rating"] for h in history}
        disp_dates, disp_ratings = [], []
        last_known = history[0]["rating"]
        for i in range(window_days):
            d   = window_start + timedelta(days=i)
            key = d.strftime("%Y-%m-%d")
            if key in hist_dict:
                last_known = hist_dict[key]
            disp_dates.append(d)
            disp_ratings.append(last_known)

        date_nums = mdates.date2num(disp_dates)
        k         = min(3, len(disp_dates) - 1)
        spl       = make_interp_spline(date_nums, disp_ratings, k=k)
        x_smooth  = np.linspace(date_nums[0], date_nums[-1], 300)
        y_smooth  = spl(x_smooth)

        ax.plot(mdates.num2date(x_smooth), y_smooth,
                color=C_ACCENT, linewidth=1.2, zorder=5, solid_capstyle="round")
        y_floor = min(disp_ratings) - 5
        ax.fill_between(mdates.num2date(x_smooth), y_smooth, y_floor,
                        alpha=0.12, color=C_ACCENT, zorder=3)

        # Only mark the latest data point
        ax.scatter([disp_dates[-1]], [disp_ratings[-1]], color=C_ACCENT, s=20, zorder=6,
                   edgecolors="white", linewidths=0.8)

        ax.set_xlim(window_start - timedelta(hours=12), latest_dt + timedelta(hours=12))
        ax.set_ylim(bottom=y_floor)
        tick_interval = max(1, window_days // 7)
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=tick_interval))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
        ax.tick_params(axis="x", colors=C_MUTED, labelsize=10, rotation=30)
        ax.tick_params(axis="y", colors=C_MUTED, labelsize=10)
        ax.set_ylabel("Rating", fontsize=10, color=C_MUTED, labelpad=4)
        ax.grid(True, color=C_GRID, linewidth=0.6, linestyle="--", alpha=0.7)

        for spine in ("top", "right"):
            ax.spines[spine].set_visible(False)
        for spine in ("bottom", "left"):
            ax.spines[spine].set_color(C_LIGHT)

        ax.annotate(
            str(disp_ratings[-1]),
            xy=(disp_dates[-1], disp_ratings[-1]),
            xytext=(3, 3), textcoords="offset points",
            fontsize=12, color=C_ACCENT, fontweight="bold",
        )
    else:
        ax.axis("off")
        ax.text(0.5, 0.5, "Collecting data...\nCheck back soon!",
                ha="center", va="center", transform=ax.transAxes,
                fontsize=12, color=C_MUTED, linespacing=1.8)

    ax.set_title("Rating History", fontsize=17, color=C_ACCENT,
                 pad=5, fontweight="bold", loc="left")

    plt.savefig(ASSETS_DIR / "rating_graph.svg",
                format="svg", bbox_inches=None, pad_inches=0, transparent=True)
    plt.close()
    print("  ✓ rating_graph.svg")


# ── Main ────────────────────────────────────────────────────────────────────
def main():
    print("Fetching solved.ac data...")
    user_data     = fetch_user_data()
    problem_stats = fetch_problem_stats()

    print("Counting languages from repo...")
    lang_counts = get_language_counts()

    print("Updating rating history...")
    history = update_history(user_data)

    print("Generating SVGs...")
    generate_profile_card(user_data, lang_counts, problem_stats)
    generate_lang_list(lang_counts)
    generate_rating_graph(history, user_data)

    print(f"\nDone — {user_data['handle']} · "
          f"{tier_name(user_data['tier'])} · "
          f"Rating {user_data['rating']} · "
          f"#{user_data['rank']:,} · "
          f"{user_data['solvedCount']} solved")


if __name__ == "__main__":
    main()
