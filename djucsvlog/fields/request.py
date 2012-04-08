import djucsvlog.settings as my_settings
from djucsvlog.fields.tools import json_dump_line, readable_dict, readable_list


def path(request):
    return request.path

def language_code(request):
    return getattr(request,'LANGUAGE_CODE','')

def get(request):
    return readable_dict(request.GET) 

def post(request):
    return readable_dict(request.POST)

def files(request):
    if not request.FILES:
        return '{}'
    ret = ''
    for field,file in request.FILES.items():
        ret += '\n"%s":%s,' %(field,readable_list([file.name,file.content_type,file.size]))
    return '{'+ret[:-1]+'\n}'

def cookies(request):
    return readable_dict(request.COOKIES)

def request_form_data(request):
    ret = ''
    r_get = get(request)
    if r_get != '{}':
        ret+='\n"G":'+r_get+','
    
    r_post = post(request)
    if r_post != '{}':
        ret+='\n"P":'+r_post+','
    
    r_files = files(request)
    if r_files != '{}':
        ret+='\n"F":'+r_files+','
    if not ret:
        return '{}'
    return '{'+ret[:-1]+'\n}'

def request_data(request):
    ret = request_form_data(request)
    
    
    r_cookies = cookies(request)
    if  r_cookies == '{}':
        return ret
    
    if ret == '{}':
        return '{"C":'+r_cookies+'}'

    return ret[:-1] + ',"C":'+r_cookies+'}'

def userid(request):
    return (request.user.id or '0')

def sessionid(request):
    if hasattr(request, 'session'):
        return request.session._session_key
    return ''

def browser_uuid(request):
    from djucsvlog.glog import glog
    import uuid
    browser_uuid = request.COOKIES.get(my_settings.BROWSER_UUID_COOKIE)
    if not browser_uuid:
        browser_uuid = uuid.uuid4().get_hex()

    glog.browser_uuid = browser_uuid
    return glog.browser_uuid

def remote_addr(request):
    return request.META.get(my_settings.REQ_REMOTE_ADDR_REAL_IP,request.META.get('REMOTE_ADDR', my_settings.REQ_REMOTE_ADDR_ANONYMOUSE))

def http_host(request):
    return request.META.get('HTTP_HOST',my_settings.REQ_HTTP_HOST_NOHOST)

def http_user_agent(request):
    meta = request.META
    ret =  meta.get('HTTP_USER_AGENT','NO USER AGENT')
    if 'HTTP_ACCEPT_LANGUAGE' in meta:
        ret+= ' Accept Language:'+meta['HTTP_ACCEPT_LANGUAGE']
    if 'HTTP_ACCEPT_ENCODING' in meta:
        ret += ' Accept Encoding:'+meta['HTTP_ACCEPT_ENCODING']
    return ret

def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k.
    Stolen from http://stackoverflow.com/questions/519633/lazy-method-for-reading-big-file-in-python
    """
    while True:
        data = file_object.read(chunk_size)
        if not data:
            file_object.seek(0)
            break
        yield data
        
import os
def find_place_to_store(name):
    from random import randint
    while True:
        full_path = os.path.join(my_settings.REQ_SAVE_FILES_FOLDER,name)
        if not os.path.exists(full_path):
            return full_path
        point_cunks = name.split('.')
        if len(point_cunks) == 1:
            #without exstension
            name += str(randint(0,9))
        else:
            #with extenstion add randint after name and before extension
            name = '%s%s.%s' % ('.'.join(point_cunks[:-1]), randint(0,9),point_cunks[-1])
            
        

def save_files(request):
    if not my_settings.REQ_SAVE_FILES_FOLDER:
        return

    if not request.FILES:
        return '{}'
    ret = ''
    for field,file in request.FILES.items():
        store_filename = find_place_to_store(file.name)
        ret += '\n"%s":%s,' %(field,readable_list([file.name,store_filename,file.content_type,file.size]))
        
        fh = open(store_filename,'wb')
        for piece in read_in_chunks(file.file):
            fh.write(piece)
        fh.close()
    
    return '{'+ret+'}'
        
def http_referer(request):
    return request.META.get('HTTP_REFERER','')

def http_accept_language(request):
    return request.META.get('HTTP_ACCEPT_LANGUAGE','')

def is_ajax(request):
    return int(request.is_ajax())

def is_secure(request):
    return int(request.is_secure())