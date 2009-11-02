from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class ScheduledItem(models.Model):
    published = models.DateTimeField()
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType)
    content_object = generic.GenericForeignKey()

    class Meta(object):
        ordering = ['-published']

    def __unicode__(self):
        return "%s" % self.published

