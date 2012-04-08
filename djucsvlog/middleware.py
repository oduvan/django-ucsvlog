import sys
import datetime

from ucsvlog.utils import arr_lambda_by_name, get_trio_log, arr_funcs_call

from django.views.debug import ExceptionReporter
from django.http import Http404
from django.db import transaction
from glog import glog
import settings as my_settings
from djucsvlog.fields import request as request_fields
from djucsvlog.fields import response as response_fields
from djucsvlog.fields import exception_info as exception_fields


class LogRequestInfo(object):
    def __init__(self,*args,**kwargs):
        self.def_req_log = self.iget_def_req_log() 
        self.def_res_log = self.iget_def_res_log()
        self.mid_log,self.mid_a_log,self.mid_c_log = get_trio_log(glog,my_settings.MIDDLEWARE_LOG_NAME)
        return super(LogRequestInfo,self).__init__(*args,**kwargs)
    
    def iget_def_req_log(self):
        return arr_lambda_by_name(my_settings.REQUEST_FIELDS,request_fields)
    
    def iget_def_res_log(self):
        return arr_lambda_by_name(my_settings.RESPONSE_FIELDS,response_fields)
    
    def iget_exception_vars_max_length(self):
        return my_settings.EXCEPTION_VARS_MAX_LENGTH
    
    def process_request(self,request):
        self.mid_a_log(my_settings.REQ_LOG_NAME,arr_funcs_call(self.def_req_log,request))
    def process_response(self,request,response):
        self.mid_c_log(my_settings.REQ_LOG_NAME,arr_funcs_call(self.def_res_log,request,response))
        if my_settings.FLUSH_RESPONSE:
            glog.flush()
        if glog.browser_uuid:
            response.set_cookie(my_settings.BROWSER_UUID_COOKIE, glog.browser_uuid, max_age=my_settings.BROWSER_UUID_COOKIE_MAX_AGE)
        return response

    def _process_exception(self,exception,exR,close_name=my_settings.REQ_LOG_NAME):
        #save head exception information
        def_exc_log = arr_lambda_by_name(my_settings.EXCEPTION_FIELDS,exception_fields)
        glog.err([my_settings.EXCEPTION_TOP_NAME]+arr_funcs_call(def_exc_log,exception))
        
        #save frames info
        def_exc_log = arr_lambda_by_name(my_settings.EXCEPTION_STACK_FIELDS,exception_fields)
        frames = exR.get_traceback_frames()
        frames.reverse()
        for frame in frames:
            glog.err([my_settings.EXCEPTION_MIDDLE_NAME]+arr_funcs_call(def_exc_log,frame,exR))
        
        #save close info
        def_exc_log = arr_lambda_by_name(my_settings.EXCEPTION_CLOSE,exception_fields)
        self.mid_c_log(close_name,arr_funcs_call(def_exc_log,exception,exR))

        if my_settings.FLUSH_RESPONSE:
            glog.flush()
    
    def process_exception(self, request, exception):
        if exception.__class__ == Http404:
            return
        exR = ExceptionReporter(request,*sys.exc_info())
        try:
            transaction.rollback()
        except transaction.TransactionManagementError:
            pass
        self._process_exception(exception,exR)

class LogViewInfo(object):
    def __init__(self,*args,**kwargs): 
        self.mid_log,self.mid_a_log,self.mid_c_log = get_trio_log(glog,my_settings.MIDDLEWARE_LOG_NAME)
        return super(LogViewInfo,self).__init__(*args,**kwargs)
        
    def process_request(self,request):
        self.mid_a_log(my_settings.VIEW_LOG_NAME,arr_funcs_call(arr_lambda_by_name(my_settings.VIEW_OPEN_FIELDS,request_fields),request))
    
        
        

