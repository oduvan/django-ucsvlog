'''
djucsvlog.components.sql

Stores all sql requests for a debug mode ( DEBUG = True )
'''

from django.db.backends import util
from djucsvlog.middleware import glog
import time


class DatabaseStatTracker(util.CursorDebugWrapper):
    def execute(self, sql, params=()):
        start = time.time()
        try:
            return self.cursor.execute(sql, params)
        finally:
            stop = time.time()
            glog.dbg(['SQL',stop-start,sql,params])

util.CursorDebugWrapper = DatabaseStatTracker
