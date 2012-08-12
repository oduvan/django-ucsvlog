from ucsvlog.utils import unicoder
from djucsvlog.fields.tools import json_dump_line

def estr(exception):
    return unicoder(exception)

def etype(exception):
    return unicoder(type(exception))

def sfunction(frame,exR):
    return unicoder(frame['function'])

def sfilename(frame,exR):
    return frame['filename']

def slineno(frame,exR):
    return unicoder(frame['lineno'])

def scontext_line(frame,exR):
    return frame['context_line']

def unicoder_truncate(var,length):
    
    value = unicoder(var)
    if len(value)>length:
        return value[0:length]+'...'
    return value

def svars(frame,exR):
    import djucsvlog.settings as my_settings
    vars = frame['vars']
    ret = ''
    for v in vars:
        ret += '\n'+json_dump_line(v[0]) + ':'+ json_dump_line(unicoder_truncate(v[1],my_settings.EXCEPTION_VARS_MAX_LENGTH))+','
    return '{\n'+ ret[:-1]+'\n}'

def emeta(exception,exR):
    return 'meta'
