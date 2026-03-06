from datetime import date, datetime
import unittest

from lesson_pipeline.backfill import SAFE_DEFAULTS, backfill_ready_record
from lesson_pipeline.models import ReadyRecord, ValidationError
from lesson_pipeline.qa_sync import sync_ready_records
from lesson_pipeline.reporting import generate_weekly_data_quality_report
from lesson_pipeline.router import mark_publish_ready


class ReadyValidationTests(unittest.TestCase):
    def test_router_blocks_publish_ready_when_required_fields_missing(self):
        record = ReadyRecord(lesson_id="L1", status="Draft")

        with self.assertRaises(ValidationError):
            mark_publish_ready(record)

    def test_router_marks_ready_when_complete(self):
        record = ReadyRecord(
            lesson_id="L2",
            status="Draft",
            month_id="2026-03",
            audience="teacher",
            lesson_created_at=datetime(2026, 3, 1, 10, 0, 0),
            revision_count=0,
            difficulty_tier="intermediate",
        )

        updated = mark_publish_ready(record)

        self.assertEqual(updated.status, "Ready")

    def test_qa_sync_blocks_incomplete_ready_records(self):
        good = ReadyRecord(
            lesson_id="L3",
            status="Ready",
            month_id="2026-03",
            audience="student",
            lesson_created_at=datetime(2026, 3, 1),
            revision_count=1,
            difficulty_tier="easy",
        )
        bad = ReadyRecord(lesson_id="L4", status="Ready", month_id="2026-03")

        synced, blocked = sync_ready_records([good, bad])

        self.assertEqual([r.lesson_id for r in synced], ["L3"])
        self.assertEqual(len(blocked), 1)
        self.assertIn("L4", blocked[0])

    def test_backfill_uses_source_then_safe_defaults(self):
        source_system = {
            "L5": {
                "month_id": "2026-02",
                "lesson_created_at": "2026-02-01T08:00:00",
            }
        }
        record = ReadyRecord(lesson_id="L5", status="Ready")

        backfilled = backfill_ready_record(record, source_system)

        self.assertEqual(backfilled.month_id, "2026-02")
        self.assertEqual(backfilled.audience, SAFE_DEFAULTS["audience"])
        self.assertEqual(backfilled.revision_count, SAFE_DEFAULTS["revision_count"])
        self.assertEqual(backfilled.difficulty_tier, SAFE_DEFAULTS["difficulty_tier"])
        self.assertEqual(backfilled.lesson_created_at, datetime(2026, 2, 1, 8, 0, 0))

    def test_weekly_data_quality_report_lists_incomplete_lessons(self):
        records = [
            ReadyRecord(lesson_id="L6", status="Draft"),
            ReadyRecord(
                lesson_id="L7",
                status="Ready",
                month_id="2026-03",
                audience="student",
                lesson_created_at=datetime(2026, 3, 1),
                revision_count=0,
                difficulty_tier="easy",
            ),
        ]

        report = generate_weekly_data_quality_report(records, run_date=date(2026, 3, 4))

        self.assertEqual(report["report_date"], "2026-03-04")
        self.assertEqual(report["incomplete_count"], 1)
        self.assertEqual(report["incomplete_lessons"][0]["lesson_id"], "L6")


if __name__ == "__main__":
    unittest.main()
