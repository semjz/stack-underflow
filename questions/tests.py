from django.test import TestCase
from users.models import User
from django.urls import reverse
from .models import Question, Answer


class AnswerCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )
        self.question = Question.objects.create(
            title="Test Question",
            body="This is a test question content.",
            user=self.user
        )
        self.url = reverse('questions:answer_create', args=[self.question.id])

    def test_create_answer_with_body(self):
        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Data for the POST request (only the body)
        data = {
            'body': 'This is a test answer body.'
        }

        # Send a POST request to create the answer
        response = self.client.post(self.url, data)

        # Check if the response redirects to the question detail page
        # self.assertRedirects(response, reverse('questions:question_detail', args=[self.question.id]))

        # Check if an answer object was created with the correct content
        self.assertEqual(Answer.objects.count(), 1)
        answer = Answer.objects.first()
        self.assertEqual(answer.body, 'This is a test answer body.')

        # Check if the answer is associated with the correct question and user
        self.assertEqual(answer.question, self.question)
        self.assertEqual(answer.user, self.user)
