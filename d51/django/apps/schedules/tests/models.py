from d51.django.apps.schedules.models import *
from d51.django.apps.schedules.tests.support.models import Post, Article
from d51.django.apps.schedules.tests.utils import *
from datetime import datetime
from django.test import TestCase

class TestOfSchedule(TestCase):
    def setUp(self):
        # Not sure why, but for some reason ScheduleItem table isn't getting
        # flushed properly.  We need to make sure to delete everything that's
        # left over prior to starting the tests.
        ScheduledItem.objects.all().delete()

        create_model_tables()

    def tearDown(self):
        destroy_model_tables()

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

    def test_can_return_only_one_type_of_model_on_available(self):
        [a] = random_posts(1)
        [b] = random_articles(1)

        now = datetime.now()
        ScheduledItem.objects.create(
            published=now,
            content_object=a
        )
        ScheduledItem.objects.create(
            published=now,
            content_object=b
        )

        available = ScheduledItem.objects.return_related().available(Post)
        self.assertEqual(1, available.count())
        self.assertEqual(2, ScheduledItem.objects.return_related().available().count())

    def test_model_type_can_be_passed_to_manager_available(self):
        [a] = random_posts(1)
        [b] = random_articles(1)

        now = datetime.now()
        ScheduledItem.objects.create(
            published=now,
            content_object=a
        )
        ScheduledItem.objects.create(
            published=now,
            content_object=b
        )

        available = ScheduledItem.objects.available(Post).return_related()
        self.assertEqual(1, available.count())

