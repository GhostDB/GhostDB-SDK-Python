import jsonpickle
from GhostDB.gobj import CacheObject

class CacheResponse(object):
    def __init__(self, gobj, status, message, error):
        self.Gobj = gobj
        self.Status = status
        self.Message = message
        self.Error = error

def cache_response_json_decoder(obj):
    return jsonpickle.decode(obj)