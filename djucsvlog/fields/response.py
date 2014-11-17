#response.status_code,response._headers['content-type'][1]
from djucsvlog import settings
from djucsvlog.fields.tools import readable_dict


def status(request, response):
    return response.status_code


def ctype(request, response):
    if 'content-type' not in response._headers:
        return ''
    return response._headers['content-type'][1]


def content(request, response):
    if 'content-type' not in response._headers:
        return ''
    if response._headers['content-type'][1].lower() in settings.RESPONSE_CONTENT_LOG_TYPES:
        return response.content
    return ''


def headers(request, response):
    return readable_dict(response._headers)
