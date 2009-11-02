import datetime
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class ScheduledItemQuerySet(models.query.QuerySet):
    _return_related = False

    def _clone(self, *args, **kwargs):
        c = super(self.__class__, self)._clone(*args, **kwargs)
        c._return_related = self._return_related
        return c

    def return_related(self, do=True):
        clone = self._clone()
        clone._return_related = True
        return clone

    def __getitem__(self, k):
        item = super(self.__class__, self).__getitem__(k)
        if self._return_related and isinstance(item, ScheduledItem):
            return item.content_object
        return item

    def available(self, model=None):
        query_params = {
            "published__lte": datetime.datetime.now(),
        }
        if model:
            query_params["content_type"] = ContentType.objects.get(name=model.__name__.lower())
        return self.filter(**query_params)

class ScheduledItemManager(models.Manager):
    def return_related(self):
        return self.all().return_related()

    def get_query_set(self):
        return ScheduledItemQuerySet(self.model)

    def available(self, model=None):
        return self.get_query_set().available(model)

class ScheduledItem(models.Model):
    published = models.DateTimeField()
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType)
    content_object = generic.GenericForeignKey()

    objects = ScheduledItemManager()

    class Meta(object):
        ordering = ['-published']

    def __unicode__(self):
        return "%s" % self.published

