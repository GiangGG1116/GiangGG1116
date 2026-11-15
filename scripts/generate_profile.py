"""Generate banner PNG and SVG profile sections from data/profile.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.svg_utils import (
    THEME,
    draw_card,
    draw_icon,
    draw_pill,
    draw_section_header,
    draw_text,
    estimate_text_width,
    svg_document,
    wrap_text,
)

DATA_PATH = ROOT_DIR / "data" / "profile.json"
ASSETS_DIR = ROOT_DIR / "assets"
RAW_BANNER_PATH = ASSETS_DIR / "profile-banner-raw.png"
BANNER_OUT_PATH = ASSETS_DIR / "profile-banner.png"

BOLD_FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]
ITALIC_FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Italic.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf",
]


def _pick_font(candidates: list[str], size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Return the first available TrueType font from candidates."""
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


def render_banner(banner_cfg: dict[str, str], raw_path: Path, out_path: Path) -> None:
    """Overlay crisp typography, gradient scrim, and rounded corners onto raw banner."""
    base = Image.open(raw_path).convert("RGBA")
    width, height = base.size

    # Subtle dark gradient on the left third so white text stands out cleanly
    scrim = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    scrim_draw = ImageDraw.Draw(scrim)
    fade_end = int(width * 0.58)
    for px in range(fade_end):
        t = 1.0 - (px / fade_end)
        alpha = int(120 * (t**1.6))
        scrim_draw.line([(px, 0), (px, height)], fill=(10, 18, 32, alpha))
    composed = Image.alpha_composite(base, scrim)

    # Typography overlay with subtle shadow for readability
    text_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    shadow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    text_draw = ImageDraw.Draw(text_layer)
    shadow_draw = ImageDraw.Draw(shadow_layer)

    title_font = _pick_font(BOLD_FONT_CANDIDATES, int(height * 0.116))
    subtitle_font = _pick_font(ITALIC_FONT_CANDIDATES, int(height * 0.065))

    title_x = int(width * 0.085)
    title_y = int(height * 0.35)
    sub_x = int(width * 0.165)
    sub_y = int(height * 0.56)

    shadow_draw.text((title_x + 3, title_y + 4), banner_cfg["title"], font=title_font, fill=(0, 0, 0, 170))
    shadow_draw.text((sub_x + 2, sub_y + 3), banner_cfg["subtitle"], font=subtitle_font, fill=(0, 0, 0, 160))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=6))

    text_draw.text((title_x, title_y), banner_cfg["title"], font=title_font, fill=(255, 255, 255, 250))
    text_draw.text((sub_x, sub_y), banner_cfg["subtitle"], font=subtitle_font, fill=(226, 236, 248, 240))

    composed = Image.alpha_composite(composed, shadow_layer)
    composed = Image.alpha_composite(composed, text_layer)

    # Anti-aliased rounded corners (supersampled 4x mask)
    scale = 4
    mask = Image.new("L", (width * scale, height * scale), 0)
    mask_draw = ImageDraw.Draw(mask)
    radius = int(height * 0.05) * scale
    mask_draw.rounded_rectangle([(0, 0), (width * scale - 1, height * scale - 1)], radius=radius, fill=255)
    mask = mask.resize((width, height), Image.Resampling.LANCZOS)
    composed.putalpha(mask)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    composed.save(out_path, format="PNG", optimize=True)


def render_about_me(about_cfg: dict) -> str:
    """Render the About Me 2-column SVG block."""
    width, height = 1000, 146
    parts: list[str] = [
        draw_section_header(20, 34, "wave", about_cfg["title"], icon_color="#f2c94c"),
    ]
    bio_lines = wrap_text(about_cfg["bio"], max_chars=66)
    for idx, line in enumerate(bio_lines):
        parts.append(draw_text(20, 66 + idx * 22, line, size=13.5, color=THEME["text_secondary"]))

    parts.append(
        f'  <line x1="586" y1="18" x2="586" y2="{height - 18}" '
        f'stroke="{THEME["border"]}" stroke-width="1" />'
    )

    for idx, item in enumerate(about_cfg["highlights"]):
        row_y = 24 + idx * 27
        parts.append(draw_icon(item["icon"], 606, row_y, size=16, color=item["color"]))
        parts.append(draw_text(630, row_y + 13, item["text"], size=13, color=THEME["text_secondary"]))

    return svg_document(width, height, "\n".join(parts), title="About Me")


def render_core_expertise(expertise_cfg: dict) -> str:
    """Render the 4-card Core Expertise SVG block."""
    width, height = 1000, 194
    parts: list[str] = [
        draw_section_header(20, 34, "brain", expertise_cfg["title"], icon_color="#f472b6"),
    ]

    gap = 16
    card_w = 228
    card_h = 126
    start_x = 20
    start_y = 52

    for idx, card in enumerate(expertise_cfg["cards"]):
        cx = start_x + idx * (card_w + gap)
        parts.append(draw_card(cx, start_y, card_w, card_h, rx=10))
        parts.append(
            f'  <rect x="{cx + 14:.1f}" y="{start_y + 12:.1f}" width="28" height="28" '
            f'rx="7" fill="#172840" stroke="#284266" stroke-width="1" />'
        )
        parts.append(draw_icon(card["icon"], cx + 19, start_y + 17, size=18, color=card["accent"]))

        title_lines = wrap_text(card["title"], max_chars=20)
        if len(title_lines) == 1:
            parts.append(draw_text(cx + 50, start_y + 31, title_lines[0], size=13, color=THEME["text_primary"], weight="700"))
        else:
            parts.append(draw_text(cx + 50, start_y + 23, title_lines[0], size=12.5, color=THEME["text_primary"], weight="700"))
            parts.append(draw_text(cx + 50, start_y + 38, title_lines[1], size=12.5, color=THEME["text_primary"], weight="700"))

        parts.append(
            f'  <line x1="{cx + 14:.1f}" y1="{start_y + 49:.1f}" '
            f'x2="{cx + card_w - 14:.1f}" y2="{start_y + 49:.1f}" '
            f'stroke="{THEME["border_subtle"]}" stroke-width="1" />'
        )

        for row_idx, item in enumerate(card["items"]):
            iy = start_y + 68 + row_idx * 21
            parts.append(draw_icon("check", cx + 15, iy - 11, size=13, color=THEME["check_green"]))
            parts.append(draw_text(cx + 34, iy, item, size=12, color=THEME["text_secondary"]))

    return svg_document(width, height, "\n".join(parts), title="Core Expertise")


def render_experience_and_projects(exp_cfg: dict, proj_cfg: dict) -> str:
    """Render the 2-column Professional Experience + Featured Projects SVG block."""
    width, height = 1000, 266
    parts: list[str] = []

    # Left column: Professional Experience
    left_x = 20
    left_right_edge = 464
    parts.append(draw_section_header(left_x, 34, "briefcase", exp_cfg["title"], icon_color="#d29922"))

    timeline_x = left_x + 8
    y_positions = [72, 134, 196]
    parts.append(
        f'  <line x1="{timeline_x}" y1="{y_positions[0]}" x2="{timeline_x}" y2="{y_positions[-1]}" '
        f'stroke="{THEME["border"]}" stroke-width="2" />'
    )

    for idx, item in enumerate(exp_cfg["items"]):
        iy = y_positions[idx]
        parts.append(f'  <circle cx="{timeline_x}" cy="{iy}" r="7.5" fill="#173055" />')
        parts.append(f'  <circle cx="{timeline_x}" cy="{iy}" r="4.2" fill="{THEME["accent_blue"]}" />')

        pill_markup, pill_w = draw_pill(
            x=0,
            y=iy - 11,
            label=item["period"],
            bg="#172233",
            border="#2a3a52",
            text_color="#c9d1d9",
            font_size=10.0,
            height=19.0,
            pad_x=7.0,
        )
        pill_x = left_right_edge - pill_w
        # Re-render pill anchored at right edge
        pill_markup, _ = draw_pill(
            x=pill_x,
            y=iy - 11,
            label=item["period"],
            bg="#172233",
            border="#2a3a52",
            text_color="#c9d1d9",
            font_size=10.0,
            height=19.0,
            pad_x=7.0,
        )
        parts.append(pill_markup)

        role_x = timeline_x + 16
        avail_role_w = pill_x - role_x - 10
        role_size = 12.6
        if estimate_text_width(item["role"], role_size) > avail_role_w:
            role_size = 10.9
        parts.append(draw_text(role_x, iy + 3, item["role"], size=role_size, color=THEME["text_primary"], weight="600"))
        parts.append(draw_text(role_x, iy + 22, item["summary"], size=11.5, color=THEME["text_muted"]))

    # Right column: Featured Projects
    right_x = 482
    right_edge = 980
    parts.append(
        draw_section_header(
            right_x,
            34,
            "star",
            proj_cfg["title"],
            icon_color="#facc15",
            right_text=proj_cfg["cta"],
            right_x=right_edge,
        )
    )

    card_gap = 12
    card_w = 158
    card_h = 194
    card_y = 52

    for idx, proj in enumerate(proj_cfg["items"]):
        cx = right_x + idx * (card_w + card_gap)
        parts.append(draw_card(cx, card_y, card_w, card_h, rx=10))

        # Top icon medallion
        med_x = cx + (card_w - 40) / 2.0
        parts.append(
            f'  <rect x="{med_x:.1f}" y="{card_y + 14:.1f}" width="40" height="40" '
            f'rx="10" fill="#162a46" stroke="#294872" stroke-width="1" />'
        )
        parts.append(draw_icon(proj["icon"], med_x + 9, card_y + 23, size=22, color=THEME["accent_cyan"]))

        # Title
        title_lines = wrap_text(proj["title"], max_chars=18)
        title_start_y = card_y + 74
        for t_idx, line in enumerate(title_lines[:2]):
            parts.append(
                draw_text(cx + 12, title_start_y + t_idx * 16, line, size=12.5, color=THEME["text_primary"], weight="700")
            )

        # Description
        desc_start_y = title_start_y + len(title_lines[:2]) * 16 + 6
        desc_lines = wrap_text(proj["description"], max_chars=23)
        for d_idx, line in enumerate(desc_lines[:3]):
            parts.append(draw_text(cx + 12, desc_start_y + d_idx * 14, line, size=10.8, color=THEME["text_muted"]))

        # Bottom tag pills
        px = cx + 10
        py = card_y + card_h - 28
        for tag in proj["tags"]:
            tag_bg = "#192438" if not tag.get("dot") else "#14263b"
            tag_markup, tag_w = draw_pill(
                x=px,
                y=py,
                label=tag["label"],
                bg=tag_bg,
                border="#283a55",
                text_color="#d0d7de",
                dot_color=tag["color"] if tag.get("dot") else None,
                font_size=9.0,
                height=17.5,
                pad_x=4.8,
            )
            parts.append(tag_markup)
            px += tag_w + 3.5

    return svg_document(width, height, "\n".join(parts), title="Professional Experience & Featured Projects")


def render_tech_and_exploring(tech_cfg: dict, exploring_cfg: dict) -> str:
    """Render the Tech Stack & Currently Exploring 2-column SVG block."""
    width, height = 1000, 152
    parts: list[str] = []

    # Left card: Tech Stack
    left_x, left_y, left_w, left_h = 20, 12, 608, 128
    parts.append(draw_card(left_x, left_y, left_w, left_h, rx=10))
    parts.append(draw_section_header(left_x + 16, left_y + 30, "wrench", tech_cfg["title"], icon_color="#38bdf8"))

    px = left_x + 16
    py = left_y + 48
    max_x = left_x + left_w - 16
    for item in tech_cfg["items"]:
        pill_markup, pill_w = draw_pill(
            x=px,
            y=py,
            label=item["label"],
            bg="#162030",
            border="#2a3a52",
            text_color="#e6edf3",
            dot_color=item["color"],
            font_size=11.0,
            height=24.0,
            pad_x=9.0,
        )
        if px + pill_w > max_x:
            px = left_x + 16
            py += 32.0
            pill_markup, pill_w = draw_pill(
                x=px,
                y=py,
                label=item["label"],
                bg="#162030",
                border="#2a3a52",
                text_color="#e6edf3",
                dot_color=item["color"],
                font_size=11.0,
                height=24.0,
                pad_x=9.0,
            )
        parts.append(pill_markup)
        px += pill_w + 8.0

    # Right card: Currently Exploring
    right_x, right_y, right_w, right_h = 644, 12, 336, 128
    parts.append(draw_card(right_x, right_y, right_w, right_h, rx=10))
    parts.append(draw_section_header(right_x + 16, right_y + 30, "rocket", exploring_cfg["title"], icon_color="#fb7185"))

    for idx, item in enumerate(exploring_cfg["items"]):
        iy = right_y + 56 + idx * 19
        parts.append(f'  <circle cx="{right_x + 22}" cy="{iy - 4}" r="3" fill="{THEME["accent_blue"]}" />')
        parts.append(draw_text(right_x + 34, iy, item, size=12.0, color=THEME["text_secondary"]))

    return svg_document(width, height, "\n".join(parts), title="Tech Stack & Currently Exploring")


def generate_all(data_path: Path = DATA_PATH, assets_dir: Path = ASSETS_DIR) -> list[Path]:
    """Generate all static profile assets and return written paths."""
    profile = json.loads(data_path.read_text(encoding="utf-8"))
    written: list[Path] = []

    raw_banner = assets_dir / "profile-banner-raw.png"
    banner_out = assets_dir / "profile-banner.png"
    if raw_banner.exists():
        render_banner(profile["banner"], raw_banner, banner_out)
        written.append(banner_out)

    svg_outputs = {
        "about-me.svg": render_about_me(profile["about"]),
        "core-expertise.svg": render_core_expertise(profile["expertise"]),
        "experience-projects.svg": render_experience_and_projects(profile["experience"], profile["projects"]),
        "tech-exploring.svg": render_tech_and_exploring(profile["tech_stack"], profile["exploring"]),
    }

    for filename, svg_content in svg_outputs.items():
        target = assets_dir / filename
        target.write_text(svg_content, encoding="utf-8")
        written.append(target)

    return written


if __name__ == "__main__":
    paths = generate_all()
    for p in paths:
        print(f"Generated {p.relative_to(ROOT_DIR)}")
