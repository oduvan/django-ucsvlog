'''
djucsvlog.components.change_model

saves all changes in a model

all models and fields should be set in UCSVLOG_CHANGE_MODEL.

For example:

UCSVLOG_CHANGE_MODEL = [
    {
        'model':'statistics.Banner', # app.model
        'props':['pk','name','campaign.pk','campaign','picture.url'] # property of objects
    },
    {
        'model':'statistics.UserProfile',
        'props':['user.pk','user.username','balance']
    }
]
'''

from djucsvlog import glog
from djucsvlog import settings as S

from django.utils.importlib import import_module
from django.db.models import signals

assert S.CHANGE_MODEL, 'UCSVLOG_CHANGE_MODEL is not defined'

def log_prop_instance(instance,prop):
    if callable(prop):
        return prop(instance)
    val = instance
    for prop_chank in prop.split('.'):
        val = getattr(val,prop_chank,None)
    return val


def gen_model_post_save(log_func,item, model):
    def model_post_save(instance,created,raw,log_func=log_func,item=item, model=model,**kwargs):
        if raw:
            return
        log_func([S.CHANGE_MODEL_LOG_START,\
                      S.CHANGE_MODEL_LOG_CREATED if created else S.CHANGE_MODEL_LOG_UPDATED,\
                      item['model']
                      ] + [log_prop_instance(instance,prop) for prop in item['props']])
        
    return model_post_save

def gen_model_post_delete(log_func,item, model):
    def model_pre_delete(instance,log_func=log_func,item=item, model=model,**kwargs):
        log_func([S.CHANGE_MODEL_LOG_START, S.CHANGE_MODEL_LOG_DELETED,\
                      item['model']
                      ] + [log_prop_instance(instance,prop) for prop in item.get('props_delete',S.CHANGE_MODEL_PROPS_DELETE)])
        
    return model_pre_delete


for item_num, item in enumerate(S.CHANGE_MODEL):
    assert 'model' in item, 'model key needs in %s item of UCSVLOG_CHANGE_MODEL' % (item_num, )
    assert 'props' in item, 'props key needs in %s item of UCSVLOG_CHANGE_MODEL' % (item_num, )
    app_name, model_name  = item['model'].split('.')
    
    model = getattr(import_module(app_name+'.models'),model_name)
    log_func = getattr(glog,item.get('log',S.CHANGE_MODEL_LOG))
    
    
    l_log = gen_model_post_save(log_func=log_func,item=item, model=model)
    item['_post_save'] = l_log
    signals.post_save.connect(l_log,sender=model)
    
    
    l_log = gen_model_post_delete(log_func=log_func,item=item, model=model)
    item['_post_delete'] = l_log
    signals.pre_delete.connect(l_log,sender=model)
    