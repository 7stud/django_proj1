from django.test import TestCase

# Create your tests here.

import datetime

from django.utils import timezone
from django.core.urlresolvers import reverse
from django.test.client import Client

from pollsapp.models import Poll

class PollMethodTests(TestCase):
    def test_was_published_recently_with_future_poll(self):
        """
        was_published_recently() should return False for polls
        whose pub_date is in the future
        """
        future_poll = Poll(pub_date
            = timezone.now() 
            + datetime.timedelta(days=30)
        )
        self.assertEqual(future_poll.was_published_recently(), False)

    def test_was_published_recently_with_old_poll(self):
        old_poll = Poll(pub_date
            = timezone.now() - datetime.timedelta(days=15)
        )
        self.assertEqual(old_poll.was_published_recently(), False)

    def test_was_published_recently_with_recent_poll(self):
        recent_poll = Poll(pub_date
            = timezone.now() - datetime.timedelta(days=13)
        )
        self.assertEqual(recent_poll.was_published_recently(), True)


def create_poll(question, days):
    """
    Creates a poll with the specified question, published the specified
    number of days in the future from now(negative for polls published
    in the past, positive for polls that have yet to be published).
    """
    return Poll.objects.create(  #creates and saves in one step
        question = question,
        pub_date = timezone.now() + datetime.timedelta(days=days)
    )

class PollsAppIndexViewTests(TestCase):

    def test_index_view_no_polls(self):
        response = self.client.get(
            reverse('polls:index')
        )

        #self.assertEqual(response.status_code, 200)
        #The following assert has a default parameter of 
        #status_code=200:
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(
            response.context['latest_poll_list'], 
            []
        )

    def test_index_view_with_a_past_poll(self):
        create_poll("Past poll.", -13)
        response = self.client.get(
                reverse('polls:index')
        )

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
            ['<Poll: Past poll.>']
        )
        

    def test_index_view_with_a_future_poll(self):
        create_poll("Future poll.", 10)
        response = self.client.get(
                reverse('polls:index')
        )
        
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])

    def test_index_view_with_a_future_poll_and_a_past_poll(self):
        create_poll("Future poll.", 10)
        create_poll("Past poll.", -9)
        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(
                response.context['latest_poll_list'], 
                ['<Poll: Past poll.>']
        )

    def test_index_view_with_two_past_polls(self):
        create_poll("Past poll1.", -10)
        create_poll("Past poll2.", -15)
        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
            ['<Poll: Past poll1.>', '<Poll: Past poll2.>']
        )


    
class PollsAppDetailViewTests(TestCase):

    def test_detail_view_with_a_future_poll(self):
        future_poll = create_poll("Future poll.", 10)
        response = self.client.get(reverse('polls:detail', args=(future_poll.id,)))

        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_poll(self):
        past_poll = create_poll("Past poll.", -10)
        response = self.client.get(reverse('polls:detail', args=(past_poll.id,)))

        self.assertContains(response, past_poll.question)








