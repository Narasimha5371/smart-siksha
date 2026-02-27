import unittest
from unittest.mock import MagicMock
import sys
import os
import uuid

# Add the backend directory to sys.path to allow imports from app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from sqlalchemy.orm import Session
from app.services.adaptive_learning import AdaptiveLearningEngine
from app.models.all_models import StudentProgress, Lesson, ProgressStatus

class TestAdaptiveLearningEngine(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock(spec=Session)
        self.engine = AdaptiveLearningEngine(self.mock_db)
        self.student_id = str(uuid.uuid4())

    def test_get_next_recommendations_no_lessons(self):
        """Test with no lessons in the database."""
        # Setup mocks
        def query_side_effect(model):
            mock_query = MagicMock()
            if model == StudentProgress:
                mock_query.filter.return_value.all.return_value = []
            elif model == Lesson:
                mock_query.all.return_value = []
            return mock_query

        self.mock_db.query.side_effect = query_side_effect

        recommendations = self.engine.get_next_recommendations(self.student_id)
        self.assertEqual(recommendations, [])

    def test_get_next_recommendations_basic(self):
        """Test with lessons having no prerequisites."""
        lesson1 = Lesson(id=uuid.uuid4(), complexity_level=0.1, prerequisite_id=None)
        lesson2 = Lesson(id=uuid.uuid4(), complexity_level=0.2, prerequisite_id=None)

        def query_side_effect(model):
            mock_query = MagicMock()
            if model == StudentProgress:
                mock_query.filter.return_value.all.return_value = []
            elif model == Lesson:
                mock_query.all.return_value = [lesson1, lesson2]
            return mock_query

        self.mock_db.query.side_effect = query_side_effect

        recommendations = self.engine.get_next_recommendations(self.student_id)

        self.assertEqual(len(recommendations), 2)
        # Should be sorted by complexity
        self.assertEqual(recommendations[0], lesson1)
        self.assertEqual(recommendations[1], lesson2)

    def test_get_next_recommendations_prerequisite_not_met(self):
        """Test that lessons with unmet prerequisites are not recommended."""
        prereq_id = uuid.uuid4()
        lesson1 = Lesson(id=prereq_id, complexity_level=0.1, prerequisite_id=None)
        lesson2 = Lesson(id=uuid.uuid4(), complexity_level=0.2, prerequisite_id=prereq_id)

        def query_side_effect(model):
            mock_query = MagicMock()
            if model == StudentProgress:
                # Student has not completed any lessons
                mock_query.filter.return_value.all.return_value = []
            elif model == Lesson:
                mock_query.all.return_value = [lesson1, lesson2]
            return mock_query

        self.mock_db.query.side_effect = query_side_effect

        recommendations = self.engine.get_next_recommendations(self.student_id)

        # Should only recommend lesson1 because lesson2's prerequisite is not met
        self.assertEqual(len(recommendations), 1)
        self.assertEqual(recommendations[0], lesson1)

    def test_get_next_recommendations_prerequisite_met(self):
        """Test that lessons with met prerequisites are recommended."""
        prereq_id = uuid.uuid4()
        lesson1 = Lesson(id=prereq_id, complexity_level=0.1, prerequisite_id=None)
        lesson2 = Lesson(id=uuid.uuid4(), complexity_level=0.2, prerequisite_id=prereq_id)

        def query_side_effect(model):
            mock_query = MagicMock()
            if model == StudentProgress:
                # Student has completed lesson1
                progress = StudentProgress(lesson_id=prereq_id, status=ProgressStatus.COMPLETED)
                mock_query.filter.return_value.all.return_value = [progress]
            elif model == Lesson:
                mock_query.all.return_value = [lesson1, lesson2]
            return mock_query

        self.mock_db.query.side_effect = query_side_effect

        recommendations = self.engine.get_next_recommendations(self.student_id)

        # Should only recommend lesson2 because lesson1 is already completed
        self.assertEqual(len(recommendations), 1)
        self.assertEqual(recommendations[0], lesson2)

    def test_get_next_recommendations_completed_lessons(self):
        """Test that completed lessons are not recommended."""
        lesson1 = Lesson(id=uuid.uuid4(), complexity_level=0.1, prerequisite_id=None)

        def query_side_effect(model):
            mock_query = MagicMock()
            if model == StudentProgress:
                # Student has completed lesson1
                progress = StudentProgress(lesson_id=lesson1.id, status=ProgressStatus.COMPLETED)
                mock_query.filter.return_value.all.return_value = [progress]
            elif model == Lesson:
                mock_query.all.return_value = [lesson1]
            return mock_query

        self.mock_db.query.side_effect = query_side_effect

        recommendations = self.engine.get_next_recommendations(self.student_id)

        self.assertEqual(len(recommendations), 0)

    def test_get_next_recommendations_sorting_and_limit(self):
        """Test sorting by complexity and limit parameter."""
        # Create 5 lessons with varying complexity
        lessons = [
            Lesson(id=uuid.uuid4(), complexity_level=0.5, prerequisite_id=None),
            Lesson(id=uuid.uuid4(), complexity_level=0.1, prerequisite_id=None),
            Lesson(id=uuid.uuid4(), complexity_level=0.3, prerequisite_id=None),
            Lesson(id=uuid.uuid4(), complexity_level=0.4, prerequisite_id=None),
            Lesson(id=uuid.uuid4(), complexity_level=0.2, prerequisite_id=None),
        ]

        def query_side_effect(model):
            mock_query = MagicMock()
            if model == StudentProgress:
                mock_query.filter.return_value.all.return_value = []
            elif model == Lesson:
                mock_query.all.return_value = lessons
            return mock_query

        self.mock_db.query.side_effect = query_side_effect

        # Request top 3 recommendations
        recommendations = self.engine.get_next_recommendations(self.student_id, limit=3)

        self.assertEqual(len(recommendations), 3)
        # Expected order: 0.1, 0.2, 0.3
        self.assertEqual(recommendations[0].complexity_level, 0.1)
        self.assertEqual(recommendations[1].complexity_level, 0.2)
        self.assertEqual(recommendations[2].complexity_level, 0.3)

if __name__ == '__main__':
    unittest.main()
