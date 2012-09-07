'''
djucsvlog.components.sql

Stores all sql requests for a production mode ( DEBUG = False )
'''

from django.db.backends import util
from djucsvlog.middleware import glog
import time


class DatabaseStatTracker(util.CursorWrapper):
    def execute(self, sql, params=()):
        raise ValueError('OH')
        start = time.time()
        try:
            return self.cursor.execute(sql, params)
        finally:
            stop = time.time()
            glog.dbg(['SQL',stop-start,sql,params])
util.CursorWrapper = DatabaseStatTracker
