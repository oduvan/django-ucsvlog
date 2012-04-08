#response.status_code,response._headers['content-type'][1]
from djucsvlog import settings

def status(request,response):
    return response.status_code
def ctype(request,response):
    return response._headers['content-type'][1]
def content(request,response):
    return response._headers['content-type'][1].lower() in settings.RESPONSE_CONTENT_LOG_TYPES and response.content or ''

def headers(request,response):
    import json
    return json.dumps(response._headers)
