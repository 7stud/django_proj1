import datetime

from django.test import TestCase
from pollsapp.models import Poll, Choice
from django.utils import timezone

class PollTestCase(TestCase):
    def setUp(self):
        poll = Poll.objects.create( 
            question = "What's up?",
            pub_date = timezone.now()
        )
        poll.choice_set.create(
            choice_text = "The sky.",
            votes = 0
        )
        poll.choice_set.create(
            choice_text = "Just hacking.",
            votes = 1
        )


    def test_polls_have_question(self):
        first_poll = Poll.objects.get(pk=1)
        self.assertEqual(first_poll.question, "What's up?")


    def test_polls_have_choices(self):
        first_poll = Poll.objects.get(pk=1)
        self.assertEqual(first_poll.choice_set.count(), 2)


