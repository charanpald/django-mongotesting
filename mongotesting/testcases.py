#coding: utf-8

from mongoengine.python_support import PY3
from mongoengine import connect
from mongoengine.connection import connect, disconnect, get_connection

try:
    from django.test import TestCase
    from django.conf import settings
except Exception as err:
    if PY3:
        from unittest import TestCase
        # Dummy value so no error
        class settings:
            MONGO_DATABASE_NAME = 'dummy'
    else:
        raise err


class MongoTestCase(TestCase):
    """
    TestCase class that clear the collection between the tests
    """
    
    def _pre_setup(self):
        # Disconnect from current database 
        disconnect()
        connect(settings.MONGO_TEST_DATABASE, port=settings.MONGO_PORT)   
        super(MongoTestCase, self)._pre_setup()

    def _post_teardown(self):
        connection = get_connection()
        connection.drop_database(settings.MONGO_TEST_DATABASE)
        connection.close()
        super(MongoTestCase, self)._post_teardown()

