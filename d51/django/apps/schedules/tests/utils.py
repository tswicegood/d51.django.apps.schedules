import d51.django.apps.schedules.tests.support
from d51.django.apps.schedules.tests.support.models import Post, Article
from django.core.management.color import no_style
from django.core.management.sql import sql_create, sql_delete, sql_indexes
from django.db import connection
import random
import re

__all__ = [
    'create_model_tables',
    'destroy_model_tables',
    'random_models',
    'random_posts',
    'random_articles',
]

def execute_sql(statements):
    cursor = connection.cursor()
    for sql in statements:
        cursor.execute(sql)

def create_model_tables():
    """
    Create the table for the provided model(s)

    Yes, yes, yes.  This *should* be part of Django.  Instead, this logic is
    locked down like porn star with an STD inside the `django.core.management`
    command, so we've got the logic here.
    """
    style = no_style()
    app = d51.django.apps.schedules.tests.support.models
    statements = sql_create(app, style) + sql_indexes(app, style)
    execute_sql(statements)

def destroy_model_tables():
    try:
        statements = sql_delete(d51.django.apps.schedules.tests.support.models, no_style())
        execute_sql(statements)
    except Exception, e:
        # Postgres seems to like to pretend that the table isn't there, even
        # when the database says it is.  We're catching this error here to keep
        # everyone happy.  "Pick your battles" I believe is the phrase.
        if re.search('table "[a-z_]+" does not exist', str(e)):
                return
        raise e


def random_models(number, model):
    return [model.objects.create(title=str(random.randint(1*i, 100*i))) for i in range(number)]

def random_posts(number):
    return random_models(number, Post)

def random_articles(number):
    return random_models(number, Article)

