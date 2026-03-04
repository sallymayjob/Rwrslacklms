import unittest

from verification.validation.ped_06_mission_coverage import run_ped_06_mission_coverage_check


class TestPed06MissionCoverage(unittest.TestCase):
    def test_passes_with_direct_manager_evidence(self):
        payload = {
            "doc_link": "https://example.com/doc",
            "goals_day_30": "Learn team workflow",
            "goals_day_60": "Own first project",
            "goals_day_90": "Improve delivery metrics",
            "relationship_goal_month_1": "Meet all stakeholders",
            "relationship_goal_month_2": "Run weekly manager sync",
            "relationship_goal_month_3": "Host cross-team retrospective",
            "manager_share_evidence": "slack-permalink",
        }

        result = run_ped_06_mission_coverage_check(payload)
        self.assertTrue(result.passed)
        self.assertEqual(result.check_id, "PED-06")
        self.assertEqual(result.missing_requirements, [])

    def test_passes_with_privacy_safe_structured_confirmation(self):
        payload = {
            "doc_link": "https://example.com/doc",
            "goals_day_30": "Goal 30",
            "goals_day_60": "Goal 60",
            "goals_day_90": "Goal 90",
            "relationship_goal_month_1": "RG1",
            "relationship_goal_month_2": "RG2",
            "relationship_goal_month_3": "RG3",
            "manager_share_structured_confirmation": {
                "manager_share_confirmed": True,
                "privacy_constraint_reason": "Policy blocks uploading screenshots",
                "share_channel": "email",
                "share_date": "2026-03-01",
                "manager_identifier": "Engineering Manager",
            },
        }

        result = run_ped_06_mission_coverage_check(payload)
        self.assertTrue(result.passed)

    def test_fails_when_coverage_has_gaps(self):
        payload = {
            "doc_link": "https://example.com/doc",
            "goals_day_30": "Goal 30",
            "relationship_goal_month_1": "RG1",
        }

        result = run_ped_06_mission_coverage_check(payload)
        self.assertFalse(result.passed)
        self.assertIn("Day 60 goal summary", result.missing_requirements)
        self.assertIn(
            "Manager share confirmation (direct evidence or privacy-safe structured confirmation)",
            result.missing_requirements,
        )


if __name__ == "__main__":
    unittest.main()
