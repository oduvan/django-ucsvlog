==============
Django-UCSVLog
==============


Django integration with `python-ucsvlog <https://github.com/oduvan/python-ucsvlog>`_, allows you easy to write and easy to parse tree-like logs from Django.

============
Requirements
============

* `Django <https://www.djangoproject.com/>`_
* `python-ucsvlog`_

============
Installation
============

* Install ``django-ucsvlog``::

    *IN WORK*

=====================
Minimal Configuration
=====================

* Add 2 Middleware classes  `'djucsvlog.middleware.LogRequestInfo'` should be the first and `'djucsvlog.middleware.LogViewInfo'` at the end of Middleware's list. So your Middlewere's settings can looks like this::

    MIDDLEWARE_CLASSES = (
        'djucsvlog.middleware.LogRequestInfo', ##ADD (at the top of list)
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'djucsvlog.middleware.LogViewInfo', ##ADD (at the bottom of list)
        # Uncomment the next line for simple clickjacking protection:
        # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

* Add ``djucsvlog`` to ``INSTALLED_APPS`` in ``settings.py``::

    INSTALLED_APPS = (
        # other apps
        "djucsvlog",
    )

* Add path to log file of your project ::

    UCSVLOG_FILE_VERSION = 'v3' #is just helps you to split different log's file versions
    UCSVLOG_FILE = '/var/log/django/my_project/{year}-{month}-{day}-'+UCSVLOG_FILE_VERSION+'.ucsv'
                # auto-rendering name of file. It mease in 19th april of 2033 log will be written into
                # /var/log/django/my_project/2033-4-19-v3.ucsv

* You can use UCSVLOG_PRINT for debug mode to see in console what will be written.

    UCSVLOG_PRINT = True

* You can install logging handler to store in ucsvlogs all logging calls::

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            },
            'ucsvlog': {
                'class': 'djucsvlog.logging.handlers.UCSVLogHandler', #custome ucsvlog handler
            }
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins', 'ucsvlog'],
                'level': 'ERROR',
                'propagate': True,
            },
            '': {
                'handlers': ['ucsvlog'],
                'propagate': True,
                'level': 'DEBUG'
            },
        }
    }

=====
Usage
=====

About how to use `python-ucsvlog`_ or `logging <http://docs.python.org/library/logging.html>`_
in your code you can read in their own documentation..

The main difference now, is that you can use lists in calling logging functions for example::

    logger.info(['SectionName', 'History'])

You can also use global ucsvlog object::

    from djucsvlog import glog
    glog('Something happens')
    glog.err('Something important')
    glog.a_log('USER_INFO', ['ID', 5678])
    glog('Name', 'Alexander')
    glog('LName', 'Lyabah')
    glog.c_log('USER_INFO')



Middleware logs
_______________

Every user's request collecting in logs. If the following settings you can configure what exactly info you want to save.

``UCSVLOG_REQUEST_FIELDS`` - this fields are storing in the first middleware ( LogRequestInfo ), 
before the others middleware will be called. 
In this fields we can save all request information, such as user's ip, 
browser version, GET or POST data etc. 

Default value is ['http_host', 'browser_uuid', 'remote_addr', 'path', 'get', 
'post', 'files', 'http_user_agent','http_referer', 'http_accept_language']

All posible functions to store in ``UCSVLOG_REQUEST_FILEDS`` you can find at 
`djucsvlog/fields/request.py <https://github.com/oduvan/django-ucsvlog/blob/master/djucsvlog/fields/request.py>`_

Some of not so obvious fields

    * ``browser_uuid`` - simple ID which is stored in cookie for identify a different browsers in logs

    * ``save_files`` - save all submited files in folder ``UCSVLOG_REQ_SAVE_FILES_FOLDER``


============================
Other configuration settings
============================

List of all possible settings you can find in file `djucsvlog/settings.py <https://github.com/oduvan/django-ucsvlog/blob/master/djucsvlog/settings.py>`_

Line::

    get('PRINT',False)

Means that with setting can be overriden in your settings.py file by UCSVLOG_PRINT setting.

==============
Other packages
==============

 * `django-ucsvlog-analytics <https://github.com/oduvan/django-ucsvlog-analytics>`_ helps you to parse and analyse log files, generated by django-ucsvlog