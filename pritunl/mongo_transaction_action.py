from constants import *
from exceptions import *
from descriptors import *
from mongo_object import MongoObject
import mongo
import pymongo
import collections
import datetime
import bson
import logging

logger = logging.getLogger(APP_NAME)

class MongoTransactionAction:
    def __init__(self, actions, func):
        self._actions = actions
        self._func = func

    def __call__(self, *args, **kwargs):
        from mongo_transaction_collection import MongoTransactionCollection
        self._actions.append([
            self._func,
            args or '',
            kwargs or '',
        ])
        return MongoTransactionCollection(self._actions)

    def __getattr__(self, name):
        if name in MONGO_ACTION_METHODS:
            return MongoTransactionAction(self._actions, name)
        raise AttributeError(
            'MongoTransactionAction instance has no attribute %r' % name)