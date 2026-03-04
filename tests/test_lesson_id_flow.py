import unittest

from src.lesson_ids import (
    parse_lesson_id,
    validate_content_record,
    normalize_submit_token,
)
from src.lms_logic import SubmitPayload, validate_submit, completion_percentage
from scripts.migrate_deep_ids import migrate_payload


class LessonIdFlowTests(unittest.TestCase):
    def test_parse_canonical_id(self):
        parsed = parse_lesson_id("M01-W02-L03")
        self.assertEqual(parsed.module, 1)
        self.assertEqual(parsed.week, 2)
        self.assertEqual(parsed.lesson, 3)
        self.assertEqual(parsed.lesson_type, "STANDARD")

    def test_parse_legacy_deep_id(self):
        parsed = parse_lesson_id("M01-W00-DEEP")
        self.assertEqual(parsed.lesson_id, "M01-W00-L00")
        self.assertEqual(parsed.lesson_type, "DEEP")

    def test_validate_content_deep_rules(self):
        validate_content_record({"lesson_id": "M01-W00-L00", "lesson_type": "DEEP"})
        with self.assertRaises(ValueError):
            validate_content_record({"lesson_id": "M01-W00-L01", "lesson_type": "DEEP"})

    def test_submit_validation_normalizes_legacy(self):
        payload = SubmitPayload(user_id="U123", lesson_token="M02-W00-DEEP")
        self.assertEqual(validate_submit(payload), "M02-W00-L00")
        self.assertEqual(normalize_submit_token("M02-W00-DEEP"), "M02-W00-L00")

    def test_progress_deduplicates_normalized_tokens(self):
        pct = completion_percentage(["M01-W00-DEEP", "M01-W00-L00", "M01-W01-L01"], 4)
        self.assertEqual(pct, 50.0)

    def test_migration_updates_lessons_and_slack_commands(self):
        payload = {
            "lessons": [
                {"lesson_id": "M01-W00-DEEP", "title": "Deep dive"},
                {"lesson_id": "M01-W01-L01", "title": "Intro", "lesson_type": "STANDARD"},
            ],
            "slack_submit_commands": ["/submit M01-W00-DEEP", "/submit M01-W01-L01"],
        }

        migrated = migrate_payload(payload)
        self.assertEqual(migrated["lessons"][0]["lesson_id"], "M01-W00-L00")
        self.assertEqual(migrated["lessons"][0]["lesson_type"], "DEEP")
        self.assertEqual(migrated["slack_submit_commands"][0], "/submit M01-W00-L00")


if __name__ == "__main__":
    unittest.main()
