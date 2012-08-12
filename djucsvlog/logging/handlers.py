import logging

class UCSVLogHandler(logging.Handler):
    @property
    def glog(self):
        from djucsvlog import glog
        return glog
        
    def flush(self):
        self.glog.flush()
    def emit(self,record):
        if isinstance(record.msg, (list, tuple)):
            msg = record.msg
        else:
            msg = self.format(record)

        from djucsvlog import settings
        log_name = settings.LOGGING_LEVELS[record.levelname]
        getattr(self.glog, log_name)(msg)

