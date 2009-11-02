from d51.django.apps.schedules.models import *
from datetime import datetime
from django.test import TestCase
import random

# these tests assume the original repo is in place with
# project.mysite available
from project.mysite.models import Post

class TestOfSchedule(TestCase):
    def test_schedules_default_to_reverse_chronological_order(self):
        [a, b, c] = [Post.objects.create(title=str(random.randint(1*i, 100*i))) for i in range(1, 4)]

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


