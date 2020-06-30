import json
from GhostDB.gobj import CacheObject
 
class CacheRequest(object):
    def __init__(self, key="", value="", ttl=-1):
        self.Gobj = CacheObject(key, value, ttl)
        
    def json_repr(self):
        return dict(Gobj=self.Gobj)

class CacheRequestJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'json_repr'):
            return obj.json_repr()
        else:
            return json.JSONEncoder.default(self, obj)            