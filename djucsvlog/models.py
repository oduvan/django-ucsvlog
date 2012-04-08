import settings as my_settings
from ucsvlog.utils import import_name

for mod in my_settings.COMPONENTS:
    try:
        __import__(mod, {}, {}, [''])
    except ImportError,e:
        raise e
