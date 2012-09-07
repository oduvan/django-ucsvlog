from django.conf import settings
set_prefix = 'UCSVLOG_' 
def get(key, default):
    globals()[key] = getattr(settings, set_prefix+key, default)
get('MIDDLEWARE_LOG_NAME','log')
get('REQ_LOG_NAME','REQ')
get('VIEW_LOG_NAME','IN')
get('EXCEPTION_TOP_NAME','TOP')
get('EXCEPTION_MIDDLE_NAME','IN')
get('VIEW_OPEN_FIELDS',['userid'])
get('REQUEST_FIELDS', ['http_host', 'browser_uuid', 'remote_addr', 'path', 'get', 'post', 'files', 'http_user_agent',
                            'http_referer', 'http_accept_language']) # request logged fields
get('RESPONSE_FIELDS',['status','ctype','content']) #response logged fields
get('EXCEPTION_FIELDS',['estr','etype'])
get('EXCEPTION_STACK_FIELDS',['sfunction','sfilename','slineno','svars'])
get('EXCEPTION_VARS_MAX_LENGTH',100)
get('EXCEPTION_CLOSE',['emeta'])
get('LOG_NAMES',['err','imp','inf','log','trc','dbg']) #name of logs, wich will be logged
get('LOG_NAMES_AV',['err','imp','inf','log','trc','dbg']) # all names of logs, wich already using in code
get('LOG_DEF','log') #default log name, wich will be called when loggaer used without attributes
get('COMPONENTS',()) # additional components for auto saving data in logs.
                    # default components you can find at djucsvlog.components.*
                    #Example:
                    #   UCSVLOG_COMPONENS = ('djucsvlog.components.sql_debug', 'djucsvlog.components.change_model')
get('BUFFERING',0) # buffering logs before saving. This setting is used in codecs.open
get('FLUSH_RESPONSE',True) # flushes all logs from buffer to file after request is finished
get('LOG_BASE',['stacksize','filename','lineno','fname']) # list of fields, which will be show in every log line
get('PRINT',False) # print logs instead of save
get('RELATED_FOLDER',None) #  file names will be saved relatively to this folder
get('FILE',None)
get('LOG_CLOSE_ROW',None) # replaces it by a close mark ( using for python-ucsvlog )


##
#Fieald settings


##
#REQ

get('REQ_REMOTE_ADDR_REAL_IP','HTTP_X_FORWARDED_FOR')
get('REQ_REMOTE_ADDR_ANONYMOUSE','A')
get('REQ_HTTP_HOST_NOHOST','_NH_')
get('REQ_SAVE_FILES_FOLDER',None)


##
#Browser uuid middleware
get('BROWSER_UUID_COOKIE','ucsvlog_follow')
get('BROWSER_UUID_COOKIE_MAX_AGE',60*60*24*256) #cookie for one year

##
#RESPONSE
get('RESPONSE_CONTENT_LOG_TYPES',['text/json','text/xml','application/json','application/xml'])


##
# Command djucsvlog_clear_old_files
get('CLEAR_OLD_FOLDER',None)
get('CLEAR_OLD_PERIOD',7) # period in days of logs keeping
get('CLEAR_OLD_ARCHIVE',None) 


###        ###
# COMPONENTS #
###        ###

##
# ChangeModel

get('CHANGE_MODEL',None)
get('CHANGE_MODEL_LOG','log')

#the rules of storing of change model information
get('CHANGE_MODEL_LOG_START','CM')
get('CHANGE_MODEL_LOG_CREATED','cr')
get('CHANGE_MODEL_LOG_UPDATED','up')
get('CHANGE_MODEL_LOG_DELETED','dl')

get('CHANGE_MODEL_PROPS_DELETE',['pk'])

###
# Logging integration
###
['err','imp','inf','log','trc','dbg']
get('LOGGING_LEVELS',{
    'DEBUG':'dbg',
    'INFO':'log',
    'WARN':'inf',
    'WARNING':'inf',
    'ERROR':'imp',
    'FATAL':'imp',
    'CRITICAL':'err'
})
get('LOGGING_STACK_SIZE', 6)