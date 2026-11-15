"""Generate adaptive Light & Dark SVG profile sections from data/profile.json."""

from __future__ import annotations

import json
from html import escape
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT_DIR / "data" / "profile.json"
OUT_DIR = ROOT_DIR / "assets" / "svg"

FONT_FAMILY = (
    "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', "
    "Helvetica, Arial, sans-serif"
)

THEMES = {
    "dark": {
        "card_bg": "#101723",
        "card_inner": "#131c2b",
        "card_border": "#243146",
        "icon_box_bg": "#14263f",
        "icon_box_border": "#264266",
        "pill_bg": "#141e2e",
        "pill_border": "#26364d",
        "pill_text": "#d0d7de",
        "text_primary": "#f0f6fc",
        "text_secondary": "#c9d1d9",
        "text_muted": "#8b949e",
        "divider": "#202c40",
        "card_divider": "#1b2638",
        "accent_blue": "#388bfd",
        "accent_link": "#58a6ff",
        "accent_cyan": "#38bdf8",
        "accent_icon": "#38bdf8",
        "check_green": "#3fb950",
        "timeline_ring": "#132c52",
        "timeline_line": "#25416b",
        "grad_color": "#60a5fa",
        "brief_color": "#f59e0b",
        "target_color": "#f85149",
        "wave_color": "#facc15",
        "brain_color": "#f472b6",
    },
    "light": {
        "card_bg": "#f6f8fa",
        "card_inner": "#ffffff",
        "card_border": "#d0d7de",
        "icon_box_bg": "#ddf4ff",
        "icon_box_border": "#b6e3ff",
        "pill_bg": "#ffffff",
        "pill_border": "#d0d7de",
        "pill_text": "#24292f",
        "text_primary": "#1f2328",
        "text_secondary": "#32383f",
        "text_muted": "#656d76",
        "divider": "#d8dee4",
        "card_divider": "#d8dee4",
        "accent_blue": "#0969da",
        "accent_link": "#0969da",
        "accent_cyan": "#0969da",
        "accent_icon": "#0969da",
        "check_green": "#1a7f37",
        "timeline_ring": "#ddf4ff",
        "timeline_line": "#9cd1ff",
        "grad_color": "#0969da",
        "brief_color": "#bf8700",
        "target_color": "#cf222e",
        "wave_color": "#eab308",
        "brain_color": "#db2777",
    },
}


def esc(value: object) -> str:
    """Escape XML special characters safely."""
    return escape(str(value or ""), quote=True)


def est_width(text: str, font_size: float) -> float:
    """Estimate rendered width of a sans-serif string in SVG coordinate units."""
    narrow = set("iljtfrI.,:;|!/'()- ")
    wide = set("mwMWQGOD@%&")
    total = 0.0
    for ch in text:
        if ch in narrow:
            total += 0.34
        elif ch in wide:
            total += 0.78
        elif ch.isupper():
            total += 0.65
        else:
            total += 0.55
    return total * font_size


def wrap_lines(text: str, max_width: float, font_size: float) -> list[str]:
    """Wrap text along word boundaries to fit max_width at font_size."""
    words = text.split()
    if not words:
        return [""]
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        if est_width(candidate, font_size) <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def svg_doc(width: int, height: int, body: str, title: str) -> str:
    """Wrap SVG elements inside a responsive transparent-canvas SVG document."""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img">\n'
        f"  <title>{esc(title)}</title>\n"
        f"{body}\n"
        f"</svg>\n"
    )


def svg_text(
    x: float,
    y: float,
    content: str,
    size: float,
    color: str,
    weight: str = "400",
    anchor: str = "start",
    italic: bool = False,
) -> str:
    """Emit a crisp SVG <text> element."""
    style = ' font-style="italic"' if italic else ""
    return (
        f'  <text x="{x:.1f}" y="{y:.1f}" fill="{color}" '
        f'font-family="{FONT_FAMILY}" font-size="{size:.1f}" '
        f'font-weight="{weight}" text-anchor="{anchor}"{style}>{esc(content)}</text>'
    )


def draw_icon(name: str, x: float, y: float, size: float, theme: dict[str, str]) -> str:
    """Render a vector UI icon translated & scaled to (x, y, size)."""
    scale = size / 24.0
    accent = theme["accent_icon"]
    paths = {
        "wave": (
            f'<path d="M7.5 11.5V6a1.5 1.5 0 0 1 3 0v4.5M10.5 10V4.5a1.5 1.5 0 0 1 3 0V10'
            f'M13.5 10V5.5a1.5 1.5 0 0 1 3 0v6.5M16.5 10.5a1.5 1.5 0 0 1 3 0V14a6.5 6.5 0 0 1-13 0v-3.5'
            f'a1.5 1.5 0 0 1 3 0" fill="{theme["wave_color"]}" fill-opacity="0.7" '
            f'stroke="{theme["wave_color"]}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M4 5.5c1-1.2 2.2-1.8 3.5-2M19.5 4.5c1 .8 1.8 1.9 2.2 3.2" fill="none" '
            f'stroke="{theme["wave_color"]}" stroke-width="1.7" stroke-linecap="round"/>'
        ),
        "graduation": (
            f'<path d="M12 4 2 9l10 5 10-5-10-5z" fill="{theme["grad_color"]}" fill-opacity="0.4" '
            f'stroke="{theme["grad_color"]}" stroke-width="1.8" stroke-linejoin="round"/>'
            f'<path d="M6 11.5v4.5c0 1.8 2.7 3.2 6 3.2s6-1.4 6-3.2v-4.5M21 10v5" fill="none" '
            f'stroke="{theme["grad_color"]}" stroke-width="1.8" stroke-linecap="round"/>'
        ),
        "briefcase": (
            f'<rect x="3" y="7" width="18" height="13" rx="2.5" fill="{theme["brief_color"]}" fill-opacity="0.35" '
            f'stroke="{theme["brief_color"]}" stroke-width="1.8"/>'
            f'<path d="M8.5 7V5A1.5 1.5 0 0 1 10 3.5h4A1.5 1.5 0 0 1 15.5 5v2M3 12h18" fill="none" '
            f'stroke="{theme["brief_color"]}" stroke-width="1.8" stroke-linecap="round"/>'
        ),
        "target": (
            f'<circle cx="12" cy="12" r="8.5" fill="{theme["target_color"]}" fill-opacity="0.18" '
            f'stroke="{theme["target_color"]}" stroke-width="1.8"/>'
            f'<circle cx="12" cy="12" r="4.5" fill="none" stroke="{theme["target_color"]}" stroke-width="1.8"/>'
            f'<circle cx="12" cy="12" r="2" fill="{theme["target_color"]}"/>'
        ),
        "brain": (
            f'<path d="M9.5 4.5A3.5 3.5 0 0 0 6 8c0 .4.1.8.2 1.2A3.2 3.2 0 0 0 4 12.2c0 1.3.8 2.4 2 2.9'
            f'-.1.3-.2.7-.2 1.1a3.3 3.3 0 0 0 3.3 3.3c1.3 0 2.4-.7 2.9-1.8V5.8A3 3 0 0 0 9.5 4.5zm5 0'
            f'A3.5 3.5 0 0 1 18 8c0 .4-.1.8-.2 1.2a3.2 3.2 0 0 1 2.2 3c0 1.3-.8 2.4-2 2.9.1.3.2.7.2 1.1'
            f'a3.3 3.3 0 0 1-3.3 3.3c-1.3 0-2.4-.7-2.9-1.8V5.8a3 3 0 0 1 2.5-1.3z" '
            f'fill="{theme["brain_color"]}" fill-opacity="0.45" stroke="{theme["brain_color"]}" stroke-width="1.7" stroke-linejoin="round"/>'
        ),
        "cpu": (
            f'<rect x="6" y="6" width="12" height="12" rx="2" fill="none" stroke="{accent}" stroke-width="1.8"/>'
            f'<rect x="9.5" y="9.5" width="5" height="5" rx="0.8" fill="{accent}"/>'
            f'<path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4" '
            f'stroke="{accent}" stroke-width="1.8" stroke-linecap="round"/>'
        ),
        "chat": (
            f'<path d="M4 6.5A2.5 2.5 0 0 1 6.5 4h11A2.5 2.5 0 0 1 20 6.5v7a2.5 2.5 0 0 1-2.5 2.5H10l-4.5 4v-4H6.5'
            f'A2.5 2.5 0 0 1 4 13.5z" fill="{accent}" fill-opacity="0.2" stroke="{accent}" stroke-width="1.8" stroke-linejoin="round"/>'
            f'<circle cx="9" cy="10" r="1.1" fill="{accent}"/>'
            f'<circle cx="12" cy="10" r="1.1" fill="{accent}"/>'
            f'<circle cx="15" cy="10" r="1.1" fill="{accent}"/>'
        ),
        "gear": (
            f'<circle cx="12" cy="12" r="3.4" fill="none" stroke="{accent}" stroke-width="1.8"/>'
            f'<path d="M12 2.5v2.3M12 19.2v2.3M4.9 4.9l1.6 1.6M17.5 17.5l1.6 1.6M2.5 12h2.3M19.2 12h2.3'
            f'M4.9 19.1l1.6-1.6M17.5 6.5l1.6-1.6" stroke="{accent}" stroke-width="2" stroke-linecap="round"/>'
            f'<circle cx="12" cy="12" r="6.8" fill="none" stroke="{accent}" stroke-width="1.4" stroke-opacity="0.65"/>'
        ),
        "database": (
            f'<ellipse cx="12" cy="6" rx="7.5" ry="3" fill="{accent}" fill-opacity="0.2" stroke="{accent}" stroke-width="1.8"/>'
            f'<path d="M4.5 6v12c0 1.66 3.36 3 7.5 3s7.5-1.34 7.5-3V6M4.5 12c0 1.66 3.36 3 7.5 3s7.5-1.34 7.5-3" '
            f'fill="none" stroke="{accent}" stroke-width="1.8"/>'
        ),
        "check": (
            f'<path d="M5 12.5 9.5 17 19 7.5" fill="none" stroke="{theme["check_green"]}" '
            f'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
        ),
        "wrench": (
            f'<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94'
            f'l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z" '
            f'fill="{accent}" fill-opacity="0.25" stroke="{accent}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
        ),
    }
    inner = paths.get(name, f'<circle cx="12" cy="12" r="6" fill="{accent}"/>')
    return f'  <g transform="translate({x:.1f}, {y:.1f}) scale({scale:.4f})">{inner}</g>'


def draw_tech_icon(name: str, x: float, y: float, size: float = 14.0) -> str:
    """Render recognizable vector tech brand icons inside Tech Stack pills."""
    scale = size / 24.0
    icons = {
        "python": (
            '<path d="M12 3c-3 0-2.8 1.3-2.8 1.3V6h2.9v.7H8S5 6.4 5 10.6s2.6 4 2.6 4H9v-2s-.1-2.5 2.5-2.5h4'
            's2.2.1 2.2-2.2V5.3S18 3 12 3zm-1.6 1.3a.7.7 0 1 1 0 1.4.7.7 0 0 1 0-1.4z" fill="#3b82f6"/>'
            '<path d="M12 21c3 0 2.8-1.3 2.8-1.3V18h-2.9v-.7H16s3 .3 3-3.9-2.6-4-2.6-4H15v2s.1 2.5-2.5 2.5h-4'
            's-2.2-.1-2.2 2.2v2.6S6 21 12 21zm1.6-1.3a.7.7 0 1 1 0-1.4.7.7 0 0 1 0 1.4z" fill="#eab308"/>'
        ),
        "pytorch": (
            '<path d="M16.2 7.2a6 6 0 1 1-8.4 0l1.6 1.6a3.8 3.8 0 1 0 5.2 0l1.6-1.6z" fill="#ee4c2c"/>'
            '<circle cx="14.8" cy="5.4" r="1.5" fill="#ee4c2c"/>'
        ),
        "docker": (
            '<path d="M3.5 13h17c0 4.2-3.2 7.2-8.5 7.2S3.5 17.2 3.5 13z" fill="#2496ed"/>'
            '<rect x="6.5" y="9.2" width="2.4" height="2.4" rx="0.4" fill="#38bdf8"/>'
            '<rect x="9.8" y="9.2" width="2.4" height="2.4" rx="0.4" fill="#38bdf8"/>'
            '<rect x="13.1" y="9.2" width="2.4" height="2.4" rx="0.4" fill="#38bdf8"/>'
            '<rect x="9.8" y="5.9" width="2.4" height="2.4" rx="0.4" fill="#0ea5e9"/>'
        ),
        "kubernetes": (
            '<polygon points="12,3 19.8,7.2 21.5,15.5 16,21 8,21 2.5,15.5 4.2,7.2" fill="#326ce5" fill-opacity="0.22" stroke="#326ce5" stroke-width="1.7"/>'
            '<circle cx="12" cy="12" r="3" fill="none" stroke="#326ce5" stroke-width="1.6"/>'
            '<path d="M12 4.5V9M12 15v4.5M5.5 9l4 2M14.5 13l4 2M18.5 9l-4 2M9.5 13l-4 2" stroke="#326ce5" stroke-width="1.4" stroke-linecap="round"/>'
        ),
        "airflow": (
            '<path d="M12 12c0-4.2 3-7.2 7.2-7.2-1 4.2-3 7.2-7.2 7.2z" fill="#06b6d4"/>'
            '<path d="M12 12c4.2 0 7.2 3 7.2 7.2-4.2-1-7.2-3-7.2-7.2z" fill="#0ea5e9"/>'
            '<path d="M12 12c0 4.2-3 7.2-7.2 7.2 1-4.2 3-7.2 7.2-7.2z" fill="#06b6d4"/>'
            '<path d="M12 12c-4.2 0-7.2-3-7.2-7.2 4.2 1 7.2 3 7.2 7.2z" fill="#0ea5e9"/>'
            '<circle cx="12" cy="12" r="1.4" fill="#ffffff"/>'
        ),
        "mlflow": (
            '<rect x="3" y="4" width="18" height="16" rx="4.5" fill="#0194e2" fill-opacity="0.2" stroke="#0194e2" stroke-width="1.7"/>'
            '<path d="M7.2 15.2V9.2l4.8 4.4 4.8-4.4v6" fill="none" stroke="#0194e2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
        ),
        "kserve": (
            '<circle cx="12" cy="12" r="8.8" fill="#0ea5e9" fill-opacity="0.18" stroke="#0ea5e9" stroke-width="1.7"/>'
            '<path d="M9.2 7.5v9M15 7.5 10.2 12 15 16.5" fill="none" stroke="#0ea5e9" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/>'
        ),
        "fastapi": (
            '<circle cx="12" cy="12" r="9.2" fill="#009688"/>'
            '<path d="M13 6.2 8.2 13h3.3l-.7 4.8 5-6.8h-3.3L13 6.2z" fill="#ffffff"/>'
        ),
        "postgresql": (
            '<path d="M7 9.5C7 6.2 9.4 4.2 12.2 4.2c2.9 0 4.8 2 4.8 5.1 0 2-.7 3.6-1.6 4.7-.5.6-.7 1.3-.7 2.2v1.6c0 1.2-.8 2-1.9 2-1 0-1.6-.7-1.6-1.7v-2.1c-2.5-.4-4.2-2.7-4.2-6.5z" fill="#336791" fill-opacity="0.26" stroke="#336791" stroke-width="1.7" stroke-linejoin="round"/>'
            '<circle cx="10.5" cy="9.2" r="1" fill="#336791"/>'
        ),
        "qdrant": (
            '<polygon points="12,3 20,7.5 20,16.5 12,21 4,16.5 4,7.5" fill="#e11d48" fill-opacity="0.2" stroke="#e11d48" stroke-width="1.8"/>'
            '<circle cx="12" cy="12" r="3.2" fill="#e11d48"/>'
        ),
        "minio": (
            '<circle cx="12" cy="12" r="8.8" fill="#f43f5e" fill-opacity="0.18" stroke="#f43f5e" stroke-width="1.7"/>'
            '<path d="M7.4 15.2V9.2l4.6 4.2 4.6-4.2v6" fill="none" stroke="#f43f5e" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/>'
        ),
        "spark": (
            '<path d="m12 2.8 2.1 5.9 6.2.2-4.9 3.8 1.7 6-5.1-3.5-5.1 3.5 1.7-6-4.9-3.8 6.2-.2z" '
            'fill="#f97316" fill-opacity="0.26" stroke="#f97316" stroke-width="1.7" stroke-linejoin="round"/>'
            '<circle cx="12" cy="11.5" r="2.1" fill="#f97316"/>'
        ),
    }
    inner = icons.get(name.lower(), '<circle cx="12" cy="12" r="5" fill="#38bdf8"/>')
    return f'  <g transform="translate({x:.1f}, {y:.1f}) scale({scale:.4f})">{inner}</g>'


def section_header(x: float, y: float, icon: str, title: str, theme: dict[str, str]) -> str:
    """Render a consistent section header with icon + bold title."""
    return "\n".join([
        draw_icon(icon, x, y - 16, 20, theme),
        svg_text(x + 28, y, title, size=18.0, color=theme["text_primary"], weight="700"),
    ])


def render_about_me(cfg: dict, theme: dict[str, str]) -> str:
    """Render 2-column About Me block with vertical hairline divider."""
    width, height = 960, 138
    about = cfg["about"]
    parts = [section_header(0, 26, "wave", about["title"], theme)]

    bio_lines = wrap_lines(about["bio"], max_width=500, font_size=14.0)
    for idx, line in enumerate(bio_lines):
        parts.append(svg_text(0, 62 + idx * 22, line, size=14.0, color=theme["text_secondary"]))

    parts.append(
        f'  <line x1="534" y1="8" x2="534" y2="{height - 8}" stroke="{theme["divider"]}" stroke-width="1" />'
    )

    for idx, item in enumerate(about["highlights"]):
        ry = 14 + idx * 29
        parts.append(draw_icon(item["icon"], 558, ry, 17, theme))
        label = item.get("label", "")
        value = item.get("value", "")
        label_w = est_width(label, 13.5) + 5
        parts.append(svg_text(582, ry + 13, label, size=13.5, color=theme["text_primary"], weight="600"))
        parts.append(svg_text(582 + label_w, ry + 13, value, size=13.5, color=theme["text_secondary"]))

    return svg_doc(width, height, "\n".join(parts), title="About Me")


def render_core_expertise(cfg: dict, theme: dict[str, str]) -> str:
    """Render 4 equal-width Core Expertise cards in 1 horizontal row."""
    width, height = 960, 188
    exp = cfg["expertise"]
    parts = [section_header(0, 26, "brain", exp["title"], theme)]

    gap = 16
    card_w = 228
    card_y = 44
    card_h = 136

    for idx, card in enumerate(exp["cards"]):
        cx = idx * (card_w + gap)
        parts.append(
            f'  <rect x="{cx}" y="{card_y}" width="{card_w}" height="{card_h}" rx="10" '
            f'fill="{theme["card_bg"]}" stroke="{theme["card_border"]}" stroke-width="1" />'
        )
        parts.append(
            f'  <rect x="{cx + 14}" y="{card_y + 12}" width="30" height="30" rx="7" '
            f'fill="{theme["icon_box_bg"]}" stroke="{theme["icon_box_border"]}" stroke-width="1" />'
        )
        parts.append(draw_icon(card["icon"], cx + 20, card_y + 18, 18, theme))

        title_lines = wrap_lines(card["title"], max_width=card_w - 64, font_size=13.0)
        if len(title_lines) == 1:
            parts.append(
                svg_text(cx + 53, card_y + 32, title_lines[0], size=13.0, color=theme["text_primary"], weight="700")
            )
        else:
            parts.append(
                svg_text(cx + 53, card_y + 24, title_lines[0], size=12.6, color=theme["text_primary"], weight="700")
            )
            parts.append(
                svg_text(cx + 53, card_y + 40, title_lines[1], size=12.6, color=theme["text_primary"], weight="700")
            )

        parts.append(
            f'  <line x1="{cx + 14}" y1="{card_y + 52}" x2="{cx + card_w - 14}" y2="{card_y + 52}" '
            f'stroke="{theme["card_divider"]}" stroke-width="1" />'
        )

        for r_idx, bullet in enumerate(card["items"]):
            by = card_y + 74 + r_idx * 22
            parts.append(draw_icon("check", cx + 15, by - 11, 13, theme))
            parts.append(svg_text(cx + 34, by, bullet, size=12.3, color=theme["text_secondary"]))

    return svg_doc(width, height, "\n".join(parts), title="Core Expertise")


def render_experience_stack(cfg: dict, theme: dict[str, str]) -> str:
    """Render side-by-side Professional Experience timeline cards (left) & categorized Tech Stack card (right)."""
    width = 960
    exp = cfg["experience"]
    tech = cfg["tech_stack"]
    groups = tech.get("groups") or [{"label": "Core Stack", "icon": "wrench", "items": tech.get("items", [])}]

    card_y = 44.0
    tech_x = 444.0
    tech_w = width - tech_x
    inner_pad = 18.0
    start_x = tech_x + inner_pad
    max_x = width - inner_pad

    font_size = 12.0
    pill_h = 28.0
    pill_gap_x = 8.0
    pill_row_step = 34.0
    pills_offset_y = 30.0
    bottom_pad = 14.0

    # Pass 1: lay out Tech Stack groups to determine shared card height
    band_layouts: list[tuple[dict, float, float, list[tuple[float, float, float, dict]]]] = []
    cur_y = card_y
    for group in groups:
        px = start_x
        py = cur_y + pills_offset_y
        placed: list[tuple[float, float, float, dict]] = []
        max_py = py
        for item in group.get("items", []):
            pw = est_width(item["name"], font_size) + 40.0
            if px > start_x and px + pw > max_x:
                px = start_x
                py += pill_row_step
            placed.append((px, py, pw, item))
            max_py = max(max_py, py)
            px += pw + pill_gap_x
        band_h = (max_py - cur_y) + pill_h + bottom_pad
        band_layouts.append((group, cur_y, band_h, placed))
        cur_y += band_h

    tech_h = cur_y - card_y
    exp_items = exp.get("items", [])
    n_exp = max(len(exp_items), 1)
    exp_gap = 14.0
    exp_card_h = max(92.0, (tech_h - exp_gap * (n_exp - 1)) / n_exp)
    body_h = max(tech_h, n_exp * exp_card_h + exp_gap * (n_exp - 1))
    height = int(round(card_y + body_h + 8.0))

    parts = [
        section_header(0, 26, "briefcase", exp["title"], theme),
        section_header(tech_x, 26, "wrench", tech["title"], theme),
    ]

    # Left column: timeline spine + elevated milestone cards
    tl_x = 9.0
    exp_card_x = 26.0
    exp_card_w = tech_x - 24.0 - exp_card_x
    node_ys = [card_y + idx * (exp_card_h + exp_gap) + exp_card_h / 2.0 for idx in range(len(exp_items))]

    if len(node_ys) >= 2:
        parts.append(
            f'  <line x1="{tl_x:.1f}" y1="{node_ys[0]:.1f}" x2="{tl_x:.1f}" y2="{node_ys[-1]:.1f}" '
            f'stroke="{theme["timeline_line"]}" stroke-width="2" />'
        )

    for idx, item in enumerate(exp_items):
        cy = card_y + idx * (exp_card_h + exp_gap)
        ny = node_ys[idx]
        period = item["period"]
        is_current = "present" in period.lower()
        dot_color = theme["check_green"] if is_current else theme["accent_blue"]

        parts.append(f'  <circle cx="{tl_x:.1f}" cy="{ny:.1f}" r="8.5" fill="{theme["timeline_ring"]}" />')
        parts.append(f'  <circle cx="{tl_x:.1f}" cy="{ny:.1f}" r="4.2" fill="{dot_color}" />')

        parts.append(
            f'  <rect x="{exp_card_x:.1f}" y="{cy:.1f}" width="{exp_card_w:.1f}" height="{exp_card_h:.1f}" rx="10" '
            f'fill="{theme["card_bg"]}" stroke="{theme["card_border"]}" stroke-width="1" />'
        )

        # Period pill (top-right inside card)
        pill_right = exp_card_x + exp_card_w - 16.0
        pill_pad = 28.0 if is_current else 18.0
        pill_w = est_width(period, 10.5) + pill_pad
        pill_x = pill_right - pill_w
        pill_y = cy + 15.0
        parts.append(
            f'  <rect x="{pill_x:.1f}" y="{pill_y:.1f}" width="{pill_w:.1f}" height="22" rx="11" '
            f'fill="{theme["pill_bg"]}" stroke="{theme["pill_border"]}" stroke-width="1" />'
        )
        if is_current:
            parts.append(f'  <circle cx="{pill_x + 10.5:.1f}" cy="{pill_y + 11.0:.1f}" r="3" fill="{theme["check_green"]}" />')
            parts.append(svg_text(pill_x + 17.5, pill_y + 14.5, period, size=10.5, color=theme["pill_text"], weight="500"))
        else:
            parts.append(svg_text(pill_x + pill_w / 2.0, pill_y + 14.5, period, size=10.5, color=theme["pill_text"], weight="500", anchor="middle"))

        # Company name + Role title + Summary
        company, sep, position = item["role"].partition(" – ")
        text_x = exp_card_x + 16.0
        parts.append(svg_text(text_x, cy + 30.0, company, size=14.5, color=theme["text_primary"], weight="700"))
        if sep and position:
            parts.append(svg_text(text_x, cy + 52.0, position, size=12.8, color=theme["accent_link"], weight="600"))
            sum_y = cy + 75.0
        else:
            sum_y = cy + 56.0

        sum_lines = wrap_lines(item["summary"], max_width=exp_card_w - 32.0, font_size=12.0)
        for l_idx, line in enumerate(sum_lines[:2]):
            parts.append(svg_text(text_x, sum_y + l_idx * 15.0, line, size=12.0, color=theme["text_muted"]))

    # Right column: categorized Tech Stack card matching left height
    parts.append(
        f'  <rect x="{tech_x:.0f}" y="{card_y:.0f}" width="{tech_w:.0f}" height="{body_h:.1f}" rx="10" '
        f'fill="{theme["card_bg"]}" stroke="{theme["card_border"]}" stroke-width="1" />'
    )

    for idx, (group, ry, band_h, placed) in enumerate(band_layouts):
        if idx > 0:
            parts.append(
                f'  <line x1="{start_x:.1f}" y1="{ry:.1f}" x2="{max_x:.1f}" y2="{ry:.1f}" stroke="{theme["card_divider"]}" stroke-width="1" />'
            )

        parts.append(draw_icon(group.get("icon", "wrench"), start_x, ry + 10.5, 14.0, theme))
        parts.append(
            svg_text(start_x + 20.0, ry + 21.5, group["label"], size=12.2, color=theme["text_secondary"], weight="600")
        )

        for pill_x, pill_y, pw, item in placed:
            parts.append(
                f'  <rect x="{pill_x:.1f}" y="{pill_y:.1f}" width="{pw:.1f}" height="{pill_h:.0f}" rx="7" '
                f'fill="{theme["pill_bg"]}" stroke="{theme["pill_border"]}" stroke-width="1" />'
            )
            parts.append(draw_tech_icon(item["icon"], pill_x + 10.0, pill_y + 7.0, 14.0))
            parts.append(svg_text(pill_x + 29.0, pill_y + 18.2, item["name"], size=font_size, color=theme["pill_text"], weight="500"))

    return svg_doc(width, height, "\n".join(parts), title="Professional Experience & Tech Stack")


def main() -> None:
    """Generate Light and Dark SVG assets from data/profile.json."""
    cfg = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    generators = {
        "about-me": lambda theme: render_about_me(cfg, theme),
        "core-expertise": lambda theme: render_core_expertise(cfg, theme),
        "experience-stack": lambda theme: render_experience_stack(cfg, theme),
    }

    for section_name, builder in generators.items():
        for theme_name, theme_tokens in THEMES.items():
            out_path = OUT_DIR / f"{section_name}-{theme_name}.svg"
            out_path.write_text(builder(theme_tokens), encoding="utf-8")
            print(f"Generated {out_path.relative_to(ROOT_DIR)}")


if __name__ == "__main__":
    main()
