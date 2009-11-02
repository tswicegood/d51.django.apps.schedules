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

        available = ScheduledItem.objects.available().return_related()

        self.assertEqual(1, available.count())
        self.assertEqual(a, available[0])

    def test_you_can_call_return_related_on_manager_as_well(self):
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

        available = ScheduledItem.objects.return_related().available()

        self.assertEqual(1, available.count())
        self.assertEqual(a, available[0])

    def test_using_return_related_does_not_affect_original_querysets(self):
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

        available_queryset = ScheduledItem.objects.available()
        self.assertNotEqual(available_queryset, available_queryset.return_related())




