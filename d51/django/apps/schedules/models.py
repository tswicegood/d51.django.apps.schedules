import datetime
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class ScheduledItemQuerySet(models.query.QuerySet):
    _return_related = False

    def return_related(self, do=True):
        clone = self._clone()
        clone._return_related = True
        return clone

    def __getitem__(self, k):
        item = super(self.__class__, self).__getitem__(k)
        if self._return_related and isinstance(item, ScheduledItem):
            return item.content_object
        return item

    def available(self):
        ret = self.filter(published__lte=datetime.datetime.now())
        ret._return_related = self._return_related
        return ret

class ScheduledItemManager(models.Manager):
    def return_related(self):
        return self.all().return_related()

    def get_query_set(self):
        return ScheduledItemQuerySet(self.model)

    def available(self):
        return self.get_query_set().available()

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

