import unittest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
import sys
import os

# Add the parent directory to sys.path to allow imports from app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.sync_service import SyncService
from app.models.all_models import StudentProgress

class TestSyncService(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.service = SyncService(self.mock_db)

    def test_pull_changes_no_last_pulled_at(self):
        """Test pulling changes when no last_pulled_at timestamp is provided (full sync)."""
        user_id = "test_user_id"
        last_pulled_at = None

        # Mock data
        mock_progress = MagicMock(spec=StudentProgress)
        mock_progress.id = "progress_1"
        mock_progress.student_id = user_id
        mock_progress.updated_at = datetime.utcnow()
        mock_progress.status = "completed"
        # Since the code accesses __dict__, we must mock it explicitly
        mock_progress.__dict__ = {
            "id": mock_progress.id,
            "student_id": mock_progress.student_id,
            "updated_at": mock_progress.updated_at,
            "status": mock_progress.status
        }

        # Mock query chain
        query_mock = self.mock_db.query.return_value
        filter_mock = query_mock.filter.return_value
        filter_mock.all.return_value = [mock_progress]

        # Execute
        result = self.service.pull_changes(user_id, last_pulled_at)

        # Assertions
        self.mock_db.query.assert_called_with(StudentProgress)
        self.assertTrue(query_mock.filter.called)

        self.assertIn("changes", result)
        self.assertIn("student_progress", result["changes"])
        self.assertEqual(len(result["changes"]["student_progress"]["updated"]), 1)
        self.assertEqual(result["changes"]["student_progress"]["updated"][0]["id"], "progress_1")
        self.assertIsInstance(result["timestamp"], datetime)

    def test_pull_changes_with_last_pulled_at(self):
        """Test pulling changes with a last_pulled_at timestamp (incremental sync)."""
        user_id = "test_user_id"
        last_pulled_at = datetime.utcnow() - timedelta(days=1)

        # Mock data
        mock_progress = MagicMock(spec=StudentProgress)
        mock_progress.id = "progress_2"
        mock_progress.student_id = user_id
        mock_progress.updated_at = datetime.utcnow()
        mock_progress.status = "in_progress"
        # Since the code accesses __dict__, we must mock it explicitly
        mock_progress.__dict__ = {
            "id": mock_progress.id,
            "student_id": mock_progress.student_id,
            "updated_at": mock_progress.updated_at,
            "status": mock_progress.status
        }

        # Mock query chain
        query_mock = self.mock_db.query.return_value
        # We expect two filter calls, so we make filter return the query mock itself
        query_mock.filter.return_value = query_mock
        query_mock.all.return_value = [mock_progress]

        # Execute
        result = self.service.pull_changes(user_id, last_pulled_at)

        # Assertions
        self.mock_db.query.assert_called_with(StudentProgress)

        # Verify filter was called twice (once for user_id, once for updated_at)
        self.assertEqual(query_mock.filter.call_count, 2)

        self.assertIn("changes", result)
        self.assertEqual(len(result["changes"]["student_progress"]["updated"]), 1)
        self.assertEqual(result["changes"]["student_progress"]["updated"][0]["id"], "progress_2")

    def test_pull_changes_returns_correct_structure(self):
        """Verify the returned dictionary structure matches the expected format."""
        user_id = "test_user_id"
        last_pulled_at = None

        query_mock = self.mock_db.query.return_value
        query_mock.filter.return_value.all.return_value = []

        result = self.service.pull_changes(user_id, last_pulled_at)

        expected_keys = ["changes", "timestamp"]
        self.assertTrue(all(key in result for key in expected_keys))

        changes = result["changes"]
        self.assertIn("student_progress", changes)

        student_progress = changes["student_progress"]
        self.assertIn("created", student_progress)
        self.assertIn("updated", student_progress)
        self.assertIn("deleted", student_progress)

        self.assertIsInstance(student_progress["created"], list)
        self.assertIsInstance(student_progress["updated"], list)
        self.assertIsInstance(student_progress["deleted"], list)

if __name__ == '__main__':
    unittest.main()
