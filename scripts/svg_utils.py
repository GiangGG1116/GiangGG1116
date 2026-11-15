"""Shared SVG drawing primitives and theme tokens for GitHub profile assets."""

from __future__ import annotations

from html import escape

FONT_FAMILY = (
    "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', "
    "Helvetica, Arial, sans-serif"
)

THEME = {
    "bg_canvas": "#0d1117",
    "bg_card": "#121924",
    "bg_card_inner": "#161f2d",
    "bg_pill": "#192334",
    "border": "#263244",
    "border_subtle": "#1e293b",
    "text_primary": "#f0f6fc",
    "text_secondary": "#c9d1d9",
    "text_muted": "#8b949e",
    "accent_blue": "#388bfd",
    "accent_sky": "#58a6ff",
    "accent_cyan": "#38bdf8",
    "check_green": "#3fb950",
    "gold": "#e3b341",
}


def escape_xml(value: str) -> str:
    """Escape text for safe embedding inside SVG XML nodes."""
    return escape(value, quote=True)


def estimate_text_width(text: str, font_size: float) -> float:
    """Estimate rendered sans-serif text width in SVG units."""
    narrow = set("iljtfrI.,:;|!/' ")
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


def wrap_text(text: str, max_chars: int) -> list[str]:
    """Wrap text along word boundaries without exceeding max_chars per line."""
    words = text.split()
    if not words:
        return [""]
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        if len(candidate) <= max_chars:
            current = candidate
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def svg_document(width: int, height: int, body: str, defs: str = "", title: str = "") -> str:
    """Wrap SVG elements in a GitHub-safe vector-only SVG document."""
    title_el = f"<title>{escape_xml(title)}</title>\n  " if title else ""
    defs_el = f"<defs>\n{defs}\n  </defs>\n  " if defs else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img">\n'
        f"  {title_el}"
        f"{defs_el}"
        f'<rect width="{width}" height="{height}" rx="12" fill="{THEME["bg_canvas"]}" />\n'
        f"{body}\n"
        f"</svg>\n"
    )


def draw_card(
    x: float,
    y: float,
    width: float,
    height: float,
    rx: float = 10,
    fill: str | None = None,
    stroke: str | None = None,
    stroke_width: float = 1.0,
) -> str:
    """Render a rounded dark card rectangle."""
    fill_color = fill or THEME["bg_card"]
    stroke_color = stroke or THEME["border"]
    return (
        f'  <rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" '
        f'rx="{rx:.1f}" fill="{fill_color}" stroke="{stroke_color}" '
        f'stroke-width="{stroke_width:.1f}" />'
    )


def draw_text(
    x: float,
    y: float,
    text: str,
    size: float = 13,
    color: str | None = None,
    weight: str = "400",
    anchor: str = "start",
    style: str = "normal",
) -> str:
    """Render an SVG text element using the GitHub sans-serif font stack."""
    fill_color = color or THEME["text_secondary"]
    style_attr = f' font-style="{style}"' if style != "normal" else ""
    anchor_attr = f' text-anchor="{anchor}"' if anchor != "start" else ""
    weight_attr = f' font-weight="{weight}"' if weight != "400" else ""
    return (
        f'  <text x="{x:.1f}" y="{y:.1f}" fill="{fill_color}" '
        f'font-family="{FONT_FAMILY}" font-size="{size:.1f}"'
        f'{weight_attr}{style_attr}{anchor_attr}>{escape_xml(text)}</text>'
    )


def draw_pill(
    x: float,
    y: float,
    label: str,
    bg: str | None = None,
    border: str | None = None,
    text_color: str | None = None,
    dot_color: str | None = None,
    font_size: float = 10.5,
    height: float = 20.0,
    pad_x: float = 8.0,
) -> tuple[str, float]:
    """Render a pill badge and return (svg_markup, total_width)."""
    text_w = estimate_text_width(label, font_size)
    dot_space = 11.0 if dot_color else 0.0
    width = round(text_w + pad_x * 2 + dot_space, 1)
    fill_c = bg or THEME["bg_pill"]
    border_c = border or THEME["border"]
    txt_c = text_color or THEME["text_secondary"]
    parts = [
        f'  <rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" '
        f'rx="{height / 2:.1f}" fill="{fill_c}" stroke="{border_c}" stroke-width="1" />'
    ]
    text_x = x + pad_x
    if dot_color:
        cy = y + height / 2.0
        parts.append(f'  <circle cx="{x + pad_x + 3:.1f}" cy="{cy:.1f}" r="3.2" fill="{dot_color}" />')
        text_x += dot_space
    text_y = y + height / 2.0 + font_size * 0.34
    parts.append(draw_text(text_x, text_y, label, size=font_size, color=txt_c, weight="500"))
    return "\n".join(parts), width


def draw_icon(name: str, x: float, y: float, size: float = 18.0, color: str = "#58a6ff") -> str:
    """Render a clean pure-vector 24x24-scaled icon anchored at top-left (x, y)."""
    scale = size / 24.0
    icons: dict[str, str] = {
        "wave": (
            '<path d="M7.5 11.5V6a1.5 1.5 0 0 1 3 0v4.5M10.5 10V4.5a1.5 1.5 0 0 1 3 0V10'
            'M13.5 10V5.5a1.5 1.5 0 0 1 3 0v6.5M16.5 10.5a1.5 1.5 0 0 1 3 0V14'
            'a6.5 6.5 0 0 1-13 0v-3.5a1.5 1.5 0 0 1 3 0" '
            f'fill="{color}" opacity="0.65" stroke="{color}" stroke-width="1.8" '
            'stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M4 5.5c1-1.2 2.2-1.8 3.5-2M19.5 4.5c1 .8 1.8 1.9 2.2 3.2" '
            f'fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round"/>'
        ),
        "brain": (
            f'<path d="M9.5 4.5a3.5 3.5 0 0 0-3.5 3.5c0 .4.1.8.2 1.2A3.2 3.2 0 0 0 4 12.2'
            'c0 1.3.8 2.4 2 2.9-.1.3-.2.7-.2 1.1a3.3 3.3 0 0 0 3.3 3.3c1.3 0 2.4-.7 2.9-1.8'
            'V5.8A3 3 0 0 0 9.5 4.5zm5 0a3.5 3.5 0 0 1 3.5 3.5c0 .4-.1.8-.2 1.2'
            'A3.2 3.2 0 0 1 20 12.2c0 1.3-.8 2.4-2 2.9.1.3.2.7.2 1.1a3.3 3.3 0 0 1-3.3 3.3'
            'c-1.3 0-2.4-.7-2.9-1.8V5.8A3 3 0 0 1 14.5 4.5z" '
            f'fill="{color}" opacity="0.55" stroke="{color}" stroke-width="1.8" '
            'stroke-linejoin="round"/>'
        ),
        "briefcase": (
            f'<rect x="3" y="7" width="18" height="13" rx="2.5" fill="{color}" opacity="0.5" '
            f'stroke="{color}" stroke-width="1.8"/>'
            f'<path d="M8.5 7V5a1.5 1.5 0 0 1 1.5-1.5h4A1.5 1.5 0 0 1 15.5 5v2'
            f'M3 12h18" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round"/>'
        ),
        "star": (
            '<path d="M12 2.8l2.8 5.7 6.3.9-4.5 4.4 1.1 6.2-5.7-3-5.7 3 '
            f'1.1-6.2-4.5-4.4 6.3-.9z" fill="{color}"/>'
        ),
        "wrench": (
            '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.7-3.7'
            'a5.5 5.5 0 0 1-7.4 7.4l-6.8 6.8a1.8 1.8 0 0 1-2.5-2.5l6.8-6.8'
            f'a5.5 5.5 0 0 1 7.4-7.4z" fill="{color}" opacity="0.35" stroke="{color}" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round"/>'
        ),
        "rocket": (
            '<path d="M14.5 3.5c3.2 0 5.8 1.2 6 6-.2 2.8-2.2 5.4-4.8 7.5l-2.5 2.5-3.2-3.2'
            ' 2.5-2.5C10.5 11.4 11.8 6 14.5 3.5z" '
            f'fill="{color}" opacity="0.55" stroke="{color}" stroke-width="1.8" stroke-linejoin="round"/>'
            f'<circle cx="15.5" cy="8.5" r="1.5" fill="#f0f6fc"/>'
            f'<path d="M6.5 14.5L4 19l4.5-2.5M9.5 8.5L5.5 9l2.5 3M15 15.5l.5 3.5-3-2" '
            f'fill="none" stroke="#fbbf24" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
        ),
        "chart": (
            f'<rect x="3" y="13" width="4.2" height="7" rx="1" fill="#3fb950"/>'
            f'<rect x="9.9" y="8" width="4.2" height="12" rx="1" fill="#38bdf8"/>'
            f'<rect x="16.8" y="4" width="4.2" height="16" rx="1" fill="#a78bfa"/>'
        ),
        "grad": (
            '<path d="M12 4L2 9l10 5 10-5-10-5z" '
            f'fill="{color}" opacity="0.55" stroke="{color}" stroke-width="1.8" stroke-linejoin="round"/>'
            f'<path d="M6 11.5v4.5c0 1.8 2.7 3.2 6 3.2s6-1.4 6-3.2v-4.5M21 10v5" '
            f'fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round"/>'
        ),
        "target": (
            f'<circle cx="12" cy="12" r="8.5" fill="{color}" opacity="0.18" stroke="{color}" stroke-width="1.9"/>'
            f'<circle cx="12" cy="12" r="4.5" fill="none" stroke="{color}" stroke-width="1.9"/>'
            f'<circle cx="12" cy="12" r="2.0" fill="{color}"/>'
        ),
        "chip": (
            f'<rect x="6" y="6" width="12" height="12" rx="2.5" fill="{color}" opacity="0.2" '
            f'stroke="{color}" stroke-width="1.8"/>'
            f'<path d="M9.5 2v4M14.5 2v4M9.5 18v4M14.5 18v4M2 9.5h4M2 14.5h4M18 9.5h4M18 14.5h4" '
            f'stroke="{color}" stroke-width="1.7" stroke-linecap="round"/>'
            f'<text x="12" y="14.5" text-anchor="middle" fill="{color}" '
            'font-family="Arial, sans-serif" font-size="6.8" font-weight="700">AI</text>'
        ),
        "chat": (
            '<path d="M4 6.5A2.5 2.5 0 0 1 6.5 4h11A2.5 2.5 0 0 1 20 6.5v7A2.5 2.5 0 0 1 17.5 16H10l-4.5 4v-4H6.5A2.5 2.5 0 0 1 4 13.5z" '
            f'fill="{color}" opacity="0.2" stroke="{color}" stroke-width="1.8" stroke-linejoin="round"/>'
            f'<circle cx="9" cy="10" r="1.1" fill="{color}"/>'
            f'<circle cx="12" cy="10" r="1.1" fill="{color}"/>'
            f'<circle cx="15" cy="10" r="1.1" fill="{color}"/>'
        ),
        "gear": (
            f'<circle cx="12" cy="12" r="3.5" fill="none" stroke="{color}" stroke-width="1.9"/>'
            '<path d="M12 2.5v2.3M12 19.2v2.3M4.9 4.9l1.6 1.6M17.5 17.5l1.6 1.6'
            'M2.5 12h2.3M19.2 12h2.3M4.9 19.1l1.6-1.6M17.5 6.5l1.6-1.6" '
            f'stroke="{color}" stroke-width="2.1" stroke-linecap="round"/>'
            f'<circle cx="12" cy="12" r="6.8" fill="none" stroke="{color}" stroke-width="1.6" opacity="0.65"/>'
        ),
        "database": (
            f'<ellipse cx="12" cy="6" rx="7.5" ry="2.8" fill="{color}" opacity="0.25" '
            f'stroke="{color}" stroke-width="1.8"/>'
            f'<path d="M4.5 6v12c0 1.6 3.4 2.8 7.5 2.8s7.5-1.2 7.5-2.8V6'
            f'M4.5 12c0 1.6 3.4 2.8 7.5 2.8s7.5-1.2 7.5-2.8" '
            f'fill="none" stroke="{color}" stroke-width="1.8"/>'
        ),
        "scales": (
            f'<path d="M12 3v17M7.5 20h9M5 7h14M5 7l-2.5 6h5L5 7zm14 0l-2.5 6h5L19 7z" '
            f'fill="none" stroke="{color}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>'
        ),
        "k8s": (
            '<path d="M12 3l7.8 3.8 1.9 8.4-5.4 6.6H7.7L2.3 15.2 4.2 6.8z" '
            f'fill="{color}" opacity="0.2" stroke="{color}" stroke-width="1.7" stroke-linejoin="round"/>'
            f'<circle cx="12" cy="12" r="3" fill="none" stroke="{color}" stroke-width="1.7"/>'
            f'<path d="M12 4.5V9M12 15v4.5M5.5 9l4 2M14.5 13l4 2M18.5 9l-4 2M9.5 13l-4 2" '
            f'stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>'
        ),
        "phone": (
            f'<rect x="6.5" y="2.5" width="11" height="19" rx="2.2" fill="{color}" opacity="0.18" '
            f'stroke="{color}" stroke-width="1.8"/>'
            f'<circle cx="12" cy="18.3" r="1" fill="{color}"/>'
            f'<path d="M10 10.5c1.2-1.2 2.8-1.2 4 0M8.5 8.5c2-2 5-2 7 0" '
            f'fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round"/>'
        ),
        "check": (
            f'<path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="{color}" '
            'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
        ),
    }
    shape = icons.get(name, f'<circle cx="12" cy="12" r="6" fill="{color}"/>')
    return f'  <g transform="translate({x:.1f}, {y:.1f}) scale({scale:.4f})">{shape}</g>'


def draw_section_header(
    x: float,
    y: float,
    icon_name: str,
    title: str,
    icon_color: str = "#58a6ff",
    right_text: str | None = None,
    right_x: float | None = None,
) -> str:
    """Render a section heading with left vector icon and optional right CTA."""
    parts = [
        draw_icon(icon_name, x, y - 16, size=20, color=icon_color),
        draw_text(x + 28, y, title, size=17.5, color=THEME["text_primary"], weight="700"),
    ]
    if right_text and right_x is not None:
        parts.append(
            draw_text(
                right_x,
                y - 1,
                right_text,
                size=12.5,
                color=THEME["accent_sky"],
                weight="600",
                anchor="end",
            )
        )
    return "\n".join(parts)
