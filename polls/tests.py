import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question

def create_question(question_text, days):
    """
    Create question with given 'question_text' and published offset 'days'.
    (Negative 'days' for publishing in the past; Positive for in the future)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, published_at=time)


class QuestionModelTests(TestCase):

    def test_no_questions(self):
        """
        If no questions exist, appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No recent polls.')
        self.assertQuerysetEqual(response.context['latest_questions'], [])

    def test_past_question(self):
        """
        Questions with old 'published_at' are displayed on index page.
        """
        create_question(question_text="Past Question", days=-30)
        response = self.client.get(reverse('polls:index'))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['latest_questions'],
            ['<Question: Past Question>']
        )

    def test_was_published_recently_with_recent_question(self):
        """
        'was_published_recently()' returns True for question with
        'published_at' new than 1 day
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(published_at=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_was_published_recently_with_old_question(self):
        """
        'was_published_recently()' returns False for questions with
        'published_at' older than 1 day
        """
        time = timezone.now() - datetime.timedelta(days=1)
        old_question = Question(published_at=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_future_question(self):
        """
        'was_published_recently()' returns False for quesitons with
        'published_at' in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(published_at=time)
        self.assertIs(future_question.was_published_recently(), False)

