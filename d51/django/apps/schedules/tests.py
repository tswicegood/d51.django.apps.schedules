from d51.django.apps.schedules.models import *
from datetime import datetime
from django.test import TestCase
import random

# these tests assume the original repo is in place with
# project.mysite available
from project.mysite.models import Post

def random_posts(number):
    return [Post.objects.create(title=str(random.randint(1*i, 100*i))) for i in range(number)]

class TestOfSchedule(TestCase):
    def test_schedules_default_to_reverse_chronological_order(self):
        [a, b, c] = random_posts(3)

        now = datetime.now()
        ScheduledItem.objects.create(
            published=now,
            content_object=a
        )
        ScheduledItem.objects.create(
            published=datetime(now.year-1, now.month, now.day),
            content_object=b
        )
        ScheduledItem.objects.create(
            published=datetime(now.year+2, now.month, now.day),
            content_object=c
        )

        schedules = ScheduledItem.objects.all()
        self.assertEqual(schedules[0].content_object, c)
        self.assertEqual(schedules[1].content_object, a)
        self.assertEqual(schedules[2].content_object, b)

    def test_available_returns_models_that_are_available(self):
        [a, b] = random_posts(2)
        now = datetime.now()
        ScheduledItem.objects.create(
            published=now,
            content_object=a
        )
        ScheduledItem.objects.create(
            published=datetime(now.year+1, now.month, now.day),
            content_object=b
        )

        expected = ScheduledItem.objects.get(object_id=a.pk)
        self.assertEqual(1, ScheduledItem.objects.available().count())
        self.assertEqual(expected, ScheduledItem.objects.available()[0])

