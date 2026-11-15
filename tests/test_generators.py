"""Unit tests for profile SVG and banner generators."""

from __future__ import annotations

import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from unittest.mock import patch

from PIL import Image

from scripts.generate_profile import generate_all
from scripts.update_stats import (
    compute_donut_segments,
    compute_top_languages,
    render_github_stats_svg,
    resolve_stats,
)

ROOT_DIR = Path(__file__).resolve().parent.parent
PROFILE_PATH = ROOT_DIR / "data" / "profile.json"
BASELINE_PATH = ROOT_DIR / "data" / "stats_baseline.json"
ASSETS_DIR = ROOT_DIR / "assets"


class TestProfileGenerators(unittest.TestCase):
    def test_generated_svgs_are_valid_github_safe_xml(self) -> None:
        svg_files = [
            ASSETS_DIR / "about-me.svg",
            ASSETS_DIR / "core-expertise.svg",
            ASSETS_DIR / "experience-projects.svg",
            ASSETS_DIR / "tech-exploring.svg",
            ASSETS_DIR / "github-stats.svg",
        ]
        for svg_path in svg_files:
            with self.subTest(svg=svg_path.name):
                self.assertTrue(svg_path.exists(), f"Missing {svg_path}")
                content = svg_path.read_text(encoding="utf-8")
                self.assertNotIn("<foreignObject", content)
                self.assertNotIn("<script", content)
                root = ET.fromstring(content)
                self.assertTrue(root.tag.endswith("svg"))

    def test_expected_content_and_fixes_present(self) -> None:
        core_svg = (ASSETS_DIR / "core-expertise.svg").read_text(encoding="utf-8")
        self.assertIn("KServe, CI/CD", core_svg)
        self.assertNotIn("KSreve", core_svg)

        exp_svg = (ASSETS_DIR / "experience-projects.svg").read_text(encoding="utf-8")
        self.assertIn("Jul 2025", exp_svg)
        self.assertIn("Vietnamese Legal", exp_svg)
        self.assertIn("RAG Platform", exp_svg)
        self.assertIn("MLOps Platform", exp_svg)
        self.assertIn("vCaller", exp_svg)
        self.assertIn("View all", exp_svg)

        tech_svg = (ASSETS_DIR / "tech-exploring.svg").read_text(encoding="utf-8")
        for tech in ["Python", "Go", "Rust", "PyTorch", "Kubernetes", "Qdrant", "MinIO"]:
            self.assertIn(tech, tech_svg)

    def test_banner_generated_with_alpha_rounded_corners(self) -> None:
        banner = Image.open(ASSETS_DIR / "profile-banner.png")
        self.assertEqual(banner.size, (2172, 724))
        self.assertEqual(banner.mode, "RGBA")
        # Top-left corner pixel should be transparent from rounded corner mask
        self.assertEqual(banner.getpixel((0, 0))[3], 0)

    def test_generate_all_in_temp_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_assets = Path(tmp)
            raw = tmp_assets / "profile-banner-raw.png"
            Image.new("RGB", (600, 200), (20, 40, 80)).save(raw)
            written = generate_all(PROFILE_PATH, tmp_assets)
            self.assertEqual(len(written), 5)
            for path in written:
                self.assertTrue(path.exists())

    def test_compute_top_languages_excludes_profile_repo(self) -> None:
        repos = [
            {
                "name": "GiangGG1116",
                "languages": {"edges": [{"size": 999999, "node": {"name": "Python", "color": "#3572A5"}}]},
            },
            {
                "name": "legal-rag",
                "languages": {
                    "edges": [
                        {"size": 600, "node": {"name": "Python", "color": "#3572A5"}},
                        {"size": 300, "node": {"name": "Go", "color": "#00ADD8"}},
                        {"size": 100, "node": {"name": "Shell", "color": "#89e051"}},
                    ]
                },
            },
        ]
        langs = compute_top_languages(repos, exclude_repo_name="GiangGG1116", top_n=2)
        self.assertEqual([item["name"] for item in langs], ["Python", "Go", "Other"])
        self.assertAlmostEqual(sum(item["percent"] for item in langs), 100.0, places=1)

    def test_compute_donut_segments_sum_to_circumference(self) -> None:
        languages = [
            {"name": "Python", "percent": 54.3, "color": "#f5b041"},
            {"name": "Go", "percent": 14.2, "color": "#38bdf8"},
            {"name": "Other", "percent": 31.5, "color": "#475569"},
        ]
        segs = compute_donut_segments(languages, radius=31.0, gap=1.6)
        self.assertEqual(len(segs), 3)
        self.assertEqual(segs[0]["dash_offset"], "-0.00")
        self.assertTrue(segs[1]["dash_offset"].startswith("-"))

    def test_resolve_stats_preserves_baseline_when_only_profile_repo_public(self) -> None:
        baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
        mock_user = {
            "contributionsCollection": {
                "contributionCalendar": {
                    "totalContributions": 4,
                    "weeks": [],
                }
            },
            "repositories": {
                "nodes": [
                    {
                        "name": "GiangGG1116",
                        "isPrivate": False,
                        "languages": {"edges": [{"size": 1000, "node": {"name": "Python", "color": "#3572A5"}}]},
                    }
                ]
            },
        }
        with patch("scripts.update_stats.fetch_github_stats", return_value=mock_user):
            resolved = resolve_stats("GiangGG1116", baseline, token="dummy", has_pat=False)
        self.assertEqual(resolved["total_contributions"], 233)
        self.assertEqual(resolved["languages"][0]["name"], "Python")
        self.assertEqual(resolved["languages"][0]["percent"], 54.3)

    def test_render_github_stats_svg_valid(self) -> None:
        baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
        profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
        svg = render_github_stats_svg(baseline, profile["quote"]["lines"])
        root = ET.fromstring(svg)
        self.assertTrue(root.tag.endswith("svg"))
        self.assertIn("233", svg)
        self.assertIn("54.3%", svg)


if __name__ == "__main__":
    unittest.main()
