from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_wiki as wiki  # noqa: E402


class BuildWikiTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.original_paths = {
            name: getattr(wiki, name)
            for name in ("ROOT", "PATHWAYS", "INBOX", "SITE", "ASSETS")
        }
        wiki.ROOT = self.root
        wiki.PATHWAYS = self.root / "pathways"
        wiki.INBOX = self.root / "inbox"
        wiki.SITE = self.root / "site"
        wiki.ASSETS = wiki.SITE / "assets"

    def tearDown(self) -> None:
        for name, value in self.original_paths.items():
            setattr(wiki, name, value)
        self.tmp.cleanup()

    def test_gu_evidence_pages_use_current_upcoming_results_heading(self) -> None:
        evidence_pages = list((ROOT / "pathways" / "gu").glob("**/evidence.md"))
        self.assertTrue(evidence_pages)

        for page in evidence_pages:
            content = page.read_text(encoding="utf-8")
            self.assertNotIn("## Watch" + " list", content, page)
            self.assertIn("\n## Upcoming trial results\n", content, page)
            self.assertIn("\n### On-treatment monitoring\n", content, page)

        expected_sections = (
            "## Who this applies to",
            "## Standard options",
            "## Landmark evidence",
            "## Biomarkers",
            "## Upcoming trial results",
            "## Toxicity",
            "## Guideline references",
            "## Sources",
            "## Changelog",
        )
        for setting in (
            "bladder/adjuvant-urothelial",
            "bladder/mUC",
            "prostate/mHSPC",
            "prostate/mCRPC",
            "prostate/nmCRPC",
        ):
            content = (
                ROOT / "pathways" / "gu" / setting / "evidence.md"
            ).read_text(encoding="utf-8")
            offsets = [content.index(f"\n{section}\n") for section in expected_sections]
            self.assertEqual(offsets, sorted(offsets), setting)
            self.assertIn("<!-- .cross_trial -->", content, setting)

        sequencing_required = (
            "bladder/mUC",
            "bladder/neoadjuvant-mibc",
            "bladder/adjuvant-urothelial",
            "prostate/mHSPC",
            "prostate/mCRPC",
            "kidney/mRCC",
        )
        for setting in sequencing_required:
            content = (
                ROOT / "pathways" / "gu" / setting / "evidence.md"
            ).read_text(encoding="utf-8")
            self.assertIn("\n## Therapy sequencing\n", content, setting)

    def test_build_renders_tables_and_canonical_figure_assets_without_bottom_line(
        self,
    ) -> None:
        setting = wiki.PATHWAYS / "gu" / "kidney" / "adjuvant-ccrcc"
        figures = setting / "figures"
        figures.mkdir(parents=True)
        (figures / "keynote-564.svg").write_text("<svg></svg>", encoding="utf-8")
        (setting / "evidence.md").write_text(
            """# Adjuvant clear-cell RCC

Last reviewed: 2026-09-21
Next review: 2026-12-20
Owner: GU clinic
Purpose: Decision support
Status: current

## Guidelines
- Guideline summary
  - Recheck the published category

## Standard options
| Risk group | Option |
| --- | --- |
| High | Pembrolizumab |

## Landmark evidence
![KEYNOTE-564 landmark survival](figures/keynote-564.svg)
""",
            encoding="utf-8",
        )

        self.assertEqual(wiki.main(), 0)

        page = (
            wiki.SITE / "gu" / "kidney" / "adjuvant-ccrcc.html"
        ).read_text(encoding="utf-8")
        self.assertIn("<table>", page)
        self.assertIn("<li>Guideline summary", page)
        self.assertIn(
            "<li>Guideline summary<ul><li>Recheck the published category</li></ul></li>",
            page,
        )
        self.assertIn('<img src="figures/keynote-564.svg"', page)
        self.assertNotIn("Bottom line", page)
        self.assertTrue(
            (wiki.SITE / "gu" / "kidney" / "figures" / "keynote-564.svg").exists()
        )

    def test_build_creates_nojekyll_file(self) -> None:
        self.assertEqual(wiki.main(), 0)

        self.assertTrue((wiki.SITE / ".nojekyll").is_file())

    def test_build_places_epic_phrase_before_bottom_references(self) -> None:
        setting = wiki.PATHWAYS / "gu" / "kidney" / "adjuvant-ccrcc"
        setting.mkdir(parents=True)
        (setting / "evidence.md").write_text(
            """# Adjuvant clear-cell RCC

Last reviewed: 2026-09-21
Next review: 2026-12-20
Owner: GU clinic
Purpose: Decision support
Status: current

## Upcoming trial results

- Named trial

## Guideline references

- Guideline link

## Sources

- Primary source link

## Changelog

- 2026-09-21: Updated.
""",
            encoding="utf-8",
        )
        (setting / "dotphrase.md").write_text(
            """#adjuvantccrcc

- Counseling: Discussed options.
""",
            encoding="utf-8",
        )

        self.assertEqual(wiki.main(), 0)

        page = (
            wiki.SITE / "gu" / "kidney" / "adjuvant-ccrcc.html"
        ).read_text(encoding="utf-8")
        self.assertLess(page.index('id="dotphrase"'), page.index("Guideline references"))
        self.assertLess(page.index("Guideline references"), page.index("Primary source link"))

    def test_build_marks_cross_trial_tables_for_scannable_comparisons(self) -> None:
        setting = wiki.PATHWAYS / "gu" / "kidney" / "adjuvant-ccrcc"
        setting.mkdir(parents=True)
        (setting / "evidence.md").write_text(
            """# Adjuvant clear-cell RCC

Last reviewed: 2026-09-21
Next review: 2026-12-20
Owner: GU clinic
Purpose: Decision support
Status: current

## Landmark evidence

<!-- .cross_trial -->
| Trial | Population | Outcome |
| --- | --- | --- |
| KEYNOTE-564 | High-risk clear-cell RCC | DFS benefit |
""",
            encoding="utf-8",
        )

        self.assertEqual(wiki.main(), 0)

        page = (
            wiki.SITE / "gu" / "kidney" / "adjuvant-ccrcc.html"
        ).read_text(encoding="utf-8")
        self.assertIn('<div class="table-wrap cross_trial">', page)
        self.assertNotIn("<p>&lt;!-- .cross_trial --&gt;</p>", page)
        self.assertIn(".cross_trial", (wiki.SITE / "assets" / "wiki.css").read_text())

    def test_build_renders_annotated_phrase_select_and_calculator_controls(self) -> None:
        setting = wiki.PATHWAYS / "gu" / "kidney" / "adjuvant-ccrcc"
        setting.mkdir(parents=True)
        (setting / "evidence.md").write_text(
            """# Adjuvant clear-cell RCC

Last reviewed: 2026-09-21
Next review: 2026-12-20
Owner: GU clinic
Purpose: Decision support
Status: current

## Guideline references

- Guideline link
""",
            encoding="utf-8",
        )
        (setting / "dotphrase.md").write_text(
            """#adjuvantccrcc

- Counseling: Histology {{select:histology|Clear-cell component|Clear-cell component confirmed|Non-clear-cell or not confirmed}}. KEYNOTE-564 category: {{calc:keynote-564|KEYNOTE-564 eligibility}}.
""",
            encoding="utf-8",
        )

        self.assertEqual(wiki.main(), 0)

        page = (
            wiki.SITE / "gu" / "kidney" / "adjuvant-ccrcc.html"
        ).read_text(encoding="utf-8")
        self.assertIn('class="phrase-tools"', page)
        self.assertIn('data-phrase-controls-b64=', page)
        self.assertIn('data-phrase-control-id="histology"', page)
        self.assertIn('data-calculator-id="keynote-564"', page)
        self.assertIn('data-phrase-control="histology"', page)
        self.assertIn('data-phrase-control="keynote-564"', page)
        phrase_body = page.split('<ul class="phrase-body">', maxsplit=1)[1].split(
            "</ul>", maxsplit=1
        )[0]
        self.assertNotIn("{{select:histology", phrase_body)
        self.assertNotIn("{{calc:keynote-564", phrase_body)

    def test_build_omits_whitespace_only_phrase_tools_line(self) -> None:
        setting = wiki.PATHWAYS / "gu" / "kidney" / "adjuvant-ccrcc"
        setting.mkdir(parents=True)
        (setting / "evidence.md").write_text(
            """# Adjuvant clear-cell RCC

Last reviewed: 2026-09-21
Next review: 2026-12-20
Owner: GU clinic
Purpose: Decision support
Status: current

## Guideline references

- Guideline link
""",
            encoding="utf-8",
        )
        (setting / "dotphrase.md").write_text(
            """#adjuvantccrcc

- Counseling: Discussed surveillance.
""",
            encoding="utf-8",
        )

        self.assertEqual(wiki.main(), 0)

        page = (
            wiki.SITE / "gu" / "kidney" / "adjuvant-ccrcc.html"
        ).read_text(encoding="utf-8")
        self.assertNotIn("\n  \n  <ul class=\"phrase-body\">", page)

    def test_planned_labels_do_not_call_pages_briefs(self) -> None:
        labels = [label for settings in wiki.PLANNED.values() for label in settings]
        self.assertFalse(any("brief" in label.lower() for label in labels))
