from ucsvlog.Logger import Logger as OriginalLogger
from ucsvlog.utils import unicoder
import settings as my_settings
from django.conf import settings

if my_settings.PRINT:
    class Logger(OriginalLogger):
        def store_row(self,data):
            print ",".join(map(unicoder,data))
        def flush(self):
            pass
else:
    Logger = OriginalLogger


class DjLogger(Logger):
    def_req_log = None #fields, which will be logged in request
    def_res_log = None #fields, which will be logged in response
    def __init__(self):
        self.browser_uuid = None  # for browser uuid middleware

        super(DjLogger,self).__init__(
                    self.iget_action_log(),
                    self.iget_level(),
                    self.iget_default(),
                    self.iget_loglev(),
                    self.iget_func_fields(),
                    self.iget_buffering(),
                    self.iget_related_folder(),
                    close_row = self.iget_close_row()
                )
            
    
    def iget_related_folder(self):
        return my_settings.RELATED_FOLDER    
    def iget_buffering(self):
        return my_settings.BUFFERING    
    def iget_level(self):
        return my_settings.LOG_NAMES
    def iget_loglev(self):
        return my_settings.LOG_NAMES_AV
    def iget_action_log(self):
        return settings.UCSVLOG_FILE
    def iget_default(self):
        return my_settings.LOG_DEF
    def iget_func_fields(self):
        return my_settings.LOG_BASE
    def iget_close_row(self):
        return my_settings.LOG_CLOSE_ROW
