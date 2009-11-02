d51.django.apps.schedules
=========================
Simple, reusable Django application for handling scheduling models for display.

Usage
-----
You can use the `schedules` app to, as the name says, handle a schedule for
models.  You don't have to modify your existing models for this to work, but
you can definitely add a `schedule` property if you need to.


### `d51.django.apps.models.ScheduledItem`
The main piece of this app, the `ScheduledItem` model, uses a [generic
relationship][generic] to manage its relationship to any model.  To create
a new scheduled item:

    ScheduleItem.object.create(
        published=some_datetime_object,
        content_object=some_model
    )

You can use the `objects.available()` method to grab all ScheduledItems that
are available---i.e., models that have a `published` date that is equal or
before the current time.

### Filtering types of scheduled objects
You can also filter the type of objects that `available()` returns by passing
in an class.  For example, to get all of the `Post` objects that are available:

    ScheduledItems.objects.available(Post)

Of course, that returns all of the matching `ScheduledItem` models, but a more
common case is needing the explicit `Post` objects.  This provides that functionality
as well via the `return_related()` method.  For example, you can use:

    ScheduledItem.objects.return_related().available(Post)
    # Or
    ScheduledItem.objects.available(Post).return_related()

Both are functionality equivalent.


[generic]: http://www.djangoproject.com/documentation/models/generic_relations/

