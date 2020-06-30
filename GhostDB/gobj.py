class CacheObject(object):
    def __init__(self, key="", value="", ttl=-1):
        self.Key = key
        self.Value = value
        self.TTL = ttl
    
    def json_repr(self):
        return dict(Key=self.Key, Value=self.Value, TTL=self.TTL)