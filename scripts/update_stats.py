"""Fetch GitHub statistics (with baseline fallback) and render assets/github-stats.svg."""

from __future__ import annotations

import json
import math
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.svg_utils import (
    THEME,
    draw_card,
    draw_icon,
    draw_section_header,
    draw_text,
    svg_document,
)

PROFILE_PATH = ROOT_DIR / "data" / "profile.json"
BASELINE_PATH = ROOT_DIR / "data" / "stats_baseline.json"
OUT_PATH = ROOT_DIR / "assets" / "github-stats.svg"

HEATMAP_COLORS = [
    "#1b2330",  # level 0
    "#0e4429",  # level 1
    "#006d32",  # level 2
    "#26a641",  # level 3
    "#39d353",  # level 4
]

GRAPHQL_QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
            contributionLevel
          }
        }
      }
    }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
      nodes {
        name
        isPrivate
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges {
            size
            node {
              name
              color
            }
          }
        }
      }
    }
  }
}
"""

LEVEL_MAP = {
    "NONE": 0,
    "FIRST_QUARTILE": 1,
    "SECOND_QUARTILE": 2,
    "THIRD_QUARTILE": 3,
    "FOURTH_QUARTILE": 4,
}


def compute_top_languages(
    repo_nodes: list[dict[str, Any]],
    exclude_repo_name: str | None = None,
    top_n: int = 2,
) -> list[dict[str, Any]]:
    """Aggregate language byte totals into top_n languages plus Other."""
    totals: dict[str, int] = {}
    colors: dict[str, str] = {}

    for node in repo_nodes:
        name = (node.get("name") or "").lower()
        if exclude_repo_name and name == exclude_repo_name.lower():
            continue
        edges = (node.get("languages") or {}).get("edges") or []
        for edge in edges:
            lang_node = edge.get("node") or {}
            lang_name = lang_node.get("name")
            size = int(edge.get("size") or 0)
            if not lang_name or size <= 0:
                continue
            totals[lang_name] = totals.get(lang_name, 0) + size
            if lang_node.get("color"):
                colors[lang_name] = lang_node["color"]

    grand_total = sum(totals.values())
    if grand_total <= 0:
        return []

    ranked = sorted(totals.items(), key=lambda item: item[1], reverse=True)
    result: list[dict[str, Any]] = []
    used_pct = 0.0

    for idx, (lang_name, size) in enumerate(ranked[:top_n]):
        pct = round((size / grand_total) * 100.0, 1)
        used_pct += pct
        default_color = "#f5b041" if idx == 0 else "#38bdf8"
        result.append(
            {
                "name": lang_name,
                "percent": pct,
                "color": colors.get(lang_name, default_color),
            }
        )

    if len(ranked) > top_n:
        other_pct = round(max(0.0, 100.0 - used_pct), 1)
        if other_pct > 0:
            result.append({"name": "Other", "percent": other_pct, "color": "#475569"})
    elif result:
        # Adjust rounding residual on the largest slice so percentages sum to 100.0
        residual = round(100.0 - sum(item["percent"] for item in result), 1)
        result[0]["percent"] = round(result[0]["percent"] + residual, 1)

    return result


def extract_calendar_data(calendar: dict[str, Any]) -> tuple[int, list[list[int]], list[dict[str, Any]]]:
    """Convert GraphQL contributionCalendar payload into heatmap weeks and month labels."""
    total = int(calendar.get("totalContributions") or 0)
    raw_weeks = calendar.get("weeks") or []
    weeks: list[list[int]] = []
    months: list[dict[str, Any]] = []
    seen_month: str | None = None

    for week_idx, week in enumerate(raw_weeks[-53:]):
        days = week.get("contributionDays") or []
        col: list[int] = []
        for day in days[:7]:
            lvl_str = day.get("contributionLevel") or "NONE"
            col.append(LEVEL_MAP.get(lvl_str, 0))
            if day.get("date") and len(col) == 1:
                dt = datetime.strptime(day["date"], "%Y-%m-%d")
                label = dt.strftime("%b")
                if label != seen_month:
                    months.append({"label": label, "week_index": week_idx})
                    seen_month = label
        while len(col) < 7:
            col.append(0)
        weeks.append(col)

    return total, weeks, months


def compute_donut_segments(
    languages: list[dict[str, Any]],
    radius: float,
    gap: float = 1.6,
) -> list[dict[str, Any]]:
    """Compute SVG stroke-dasharray / stroke-dashoffset parameters for donut slices."""
    circumference = 2.0 * math.pi * radius
    non_zero = [lang for lang in languages if float(lang.get("percent", 0)) > 0]
    effective_gap = gap if len(non_zero) > 1 else 0.0

    segments: list[dict[str, Any]] = []
    offset = 0.0
    for lang in non_zero:
        pct = float(lang["percent"])
        arc_len = (pct / 100.0) * circumference
        visible_len = max(arc_len - effective_gap, 0.5)
        segments.append(
            {
                "name": lang["name"],
                "percent": pct,
                "color": lang["color"],
                "dash_array": f"{visible_len:.2f} {circumference:.2f}",
                "dash_offset": f"{-offset:.2f}",
            }
        )
        offset += arc_len
    return segments


def fetch_github_stats(username: str, token: str) -> dict[str, Any] | None:
    """Query GitHub GraphQL API for user contributions and repository languages."""
    payload = json.dumps({"query": GRAPHQL_QUERY, "variables": {"login": username}}).encode("utf-8")
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "GiangGG1116-profile-stats",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None

    user = ((body or {}).get("data") or {}).get("user")
    if not user:
        return None
    return user


def resolve_stats(
    username: str,
    baseline: dict[str, Any],
    token: str | None,
    has_pat: bool = False,
) -> dict[str, Any]:
    """Merge live GitHub data with baseline when private repos are invisible to default tokens."""
    stats = {
        "total_contributions": baseline["total_contributions"],
        "months": baseline["months"],
        "weeks": baseline["weeks"],
        "languages": baseline["languages"],
    }
    if not token:
        return stats

    user_data = fetch_github_stats(username, token)
    if not user_data:
        return stats

    calendar = ((user_data.get("contributionsCollection") or {}).get("contributionCalendar")) or {}
    live_total, live_weeks, live_months = extract_calendar_data(calendar)

    repo_nodes = ((user_data.get("repositories") or {}).get("nodes")) or []
    live_langs = compute_top_languages(repo_nodes, exclude_repo_name=username, top_n=2)

    if has_pat or live_total >= 10:
        if live_weeks:
            stats["total_contributions"] = live_total
            stats["weeks"] = live_weeks
            stats["months"] = live_months

    if live_langs:
        stats["languages"] = live_langs

    return stats


def render_github_stats_svg(stats: dict[str, Any], quote_lines: list[str]) -> str:
    """Render the complete GitHub Stats + Top Languages + Quote SVG."""
    width, height = 1000, 214
    parts: list[str] = [
        draw_section_header(20, 34, "chart", "GitHub Stats", icon_color="#3fb950"),
    ]

    # Card 1: Total Contributions & Heatmap
    c1_x, c1_y, c1_w, c1_h = 20, 50, 522, 148
    parts.append(draw_card(c1_x, c1_y, c1_w, c1_h, rx=10))
    parts.append(draw_text(c1_x + 18, c1_y + 30, "Total Contributions", size=12.0, color=THEME["text_muted"], weight="500"))
    parts.append(
        draw_text(
            c1_x + 18,
            c1_y + 76,
            str(stats["total_contributions"]),
            size=36.0,
            color=THEME["text_primary"],
            weight="700",
        )
    )
    parts.append(draw_text(c1_x + 18, c1_y + 98, "in the last year", size=11.5, color=THEME["text_muted"]))

    grid_x = c1_x + 144
    grid_y = c1_y + 48
    cell = 5.4
    gap = 1.4
    step = cell + gap

    last_label_x = -999.0
    for month in stats["months"]:
        mx = grid_x + int(month["week_index"]) * step
        if mx - last_label_x >= 18.0 and mx <= c1_x + c1_w - 16:
            parts.append(draw_text(mx, c1_y + 36, month["label"], size=9.5, color=THEME["text_muted"]))
            last_label_x = mx

    for w_idx, week in enumerate(stats["weeks"][-53:]):
        wx = grid_x + w_idx * step
        for d_idx, level in enumerate(week[:7]):
            wy = grid_y + d_idx * step
            lvl = max(0, min(4, int(level)))
            parts.append(
                f'  <rect x="{wx:.1f}" y="{wy:.1f}" width="{cell:.1f}" height="{cell:.1f}" '
                f'rx="1.2" fill="{HEATMAP_COLORS[lvl]}" />'
            )

    # Heatmap legend: Less [][][][][] More
    legend_y = c1_y + c1_h - 22
    legend_x = c1_x + c1_w - 118
    parts.append(draw_text(legend_x, legend_y + 7, "Less", size=9.5, color=THEME["text_muted"]))
    for lvl, color in enumerate(HEATMAP_COLORS):
        lx = legend_x + 27 + lvl * 10
        parts.append(f'  <rect x="{lx:.1f}" y="{legend_y:.1f}" width="7.5" height="7.5" rx="1.5" fill="{color}" />')
    parts.append(draw_text(legend_x + 81, legend_y + 7, "More", size=9.5, color=THEME["text_muted"]))

    # Card 2: Top Languages Donut Chart
    c2_x, c2_y, c2_w, c2_h = 556, 50, 244, 148
    parts.append(draw_card(c2_x, c2_y, c2_w, c2_h, rx=10))
    parts.append(draw_text(c2_x + 16, c2_y + 25, "Top Languages", size=13.0, color=THEME["text_primary"], weight="700"))

    donut_cx = c2_x + 56
    donut_cy = c2_y + 88
    donut_r = 31.0
    parts.append(
        f'  <circle cx="{donut_cx:.1f}" cy="{donut_cy:.1f}" r="{donut_r:.1f}" '
        f'fill="none" stroke="#1e293b" stroke-width="13" />'
    )
    segments = compute_donut_segments(stats["languages"], radius=donut_r, gap=1.6)
    for seg in segments:
        parts.append(
            f'  <circle cx="{donut_cx:.1f}" cy="{donut_cy:.1f}" r="{donut_r:.1f}" '
            f'fill="none" stroke="{seg["color"]}" stroke-width="13" '
            f'stroke-dasharray="{seg["dash_array"]}" stroke-dashoffset="{seg["dash_offset"]}" '
            f'transform="rotate(-90 {donut_cx:.1f} {donut_cy:.1f})" />'
        )

    for idx, lang in enumerate(stats["languages"][:3]):
        ly = c2_y + 66 + idx * 24
        parts.append(f'  <circle cx="{c2_x + 110:.1f}" cy="{ly - 4:.1f}" r="4.2" fill="{lang["color"]}" />')
        parts.append(draw_text(c2_x + 121, ly, lang["name"], size=11.5, color=THEME["text_primary"], weight="500"))
        parts.append(
            draw_text(
                c2_x + c2_w - 14,
                ly,
                f'{float(lang["percent"]):.1f}%',
                size=11.5,
                color=THEME["text_muted"],
                anchor="end",
            )
        )

    # Right area: Quote & mountain silhouette
    q_cx = 898
    parts.append(
        '  <path d="M812 198 L852 162 L884 182 L926 146 L962 178 L984 166 L984 198 Z" '
        'fill="#141e2e" opacity="0.9" />'
    )
    parts.append(
        '  <path d="M826 198 L866 174 L896 192 L936 164 L984 198 Z" '
        'fill="#19263b" opacity="0.85" />'
    )
    for idx, line in enumerate(quote_lines[:3]):
        parts.append(
            draw_text(
                q_cx - 10,
                96 + idx * 20,
                line,
                size=13.0,
                color=THEME["text_primary"],
                weight="500",
                anchor="middle",
                style="italic",
            )
        )
    parts.append(draw_icon("rocket", q_cx + 46, 122, size=17, color="#f87171"))

    return svg_document(width, height, "\n".join(parts), title="GitHub Stats & Top Languages")


def main() -> None:
    profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    token = os.environ.get("STATS_TOKEN") or os.environ.get("GITHUB_TOKEN")
    has_pat = bool(os.environ.get("STATS_TOKEN"))
    stats = resolve_stats(profile["username"], baseline, token=token, has_pat=has_pat)
    svg = render_github_stats_svg(stats, profile["quote"]["lines"])
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(svg, encoding="utf-8")
    print(f"Generated {OUT_PATH.relative_to(ROOT_DIR)}")


if __name__ == "__main__":
    main()
