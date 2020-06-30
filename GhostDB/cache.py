import logging
import requests
import json
import time
import threading
import jsonpickle
from decimal import Decimal
from GhostDB.ring import Ring 
from GhostDB.cache_request import CacheRequest, CacheRequestJsonEncoder
from GhostDB.cache_response import CacheResponse, cache_response_json_decoder

logging.basicConfig(filename="ghostdb.log")

class Cache():
    """
    The `Cache` object that provides an interface between GhostDB nodes

    You must supply a `node_file`. This is the file that contains the
    IP addresses of all servers in your fleet. You can update this file
    as needed. Any changes to this file will automatically be picked up
    by the `Cache` object.

    If `http` is not supplied then `http` defaults to `True`.
    If your fleet requires communication over `HTTPS`, then pass `False`.

    If you do not supply the `port` your GhostDB fleet is configured
    to, then it defaults to the standard port of `7991`.
    """

    _DEAD_SERVERS = []
    _REVIVE_WAIT = 30

    _API_ENDPOINT_MAP = {
        "ping": "/ping",
        "put": "/put",
        "get": "/get",
        "add": "/add",
        "delete": "/delete",
        "flush": "/flush",
        "nodeSize": "/nodeSize",
        "getSnitchMetrics": "/getSnitchMetrics",
        "getWatchdogMetrics": "/getWatchdogMetrics"
    }

    class GhostNoMoreServersError(Exception):
        """
        The error thrown when no servers in your `node_file` are
        reachable.
        """

        def __init__(self):
            Exception.__init__(
                self, 
                "[ERROR]: All nodes marked as dead: Failed to establish a connection to any servers: (Check your fleet status)"
                )
    
    class GhostKeyError(Exception):
        """
        The error thrown when they key passed to a method is not a
        valid string.
        """

        def __init__(self):
            Exception.__init__(
                self,
                "[ERROR]: Key must be of type string"
            )

    def __init__(self, nodes_file, http=True, port=7991):
        self.nodes_file = nodes_file
        self.protocol = "http://" if http else "https://"
        self.port = str(port)
        self.ring = Ring(nodes_file)
        self._server_revive()


    def get(self, key):
        """
        The `get()` method will fetch a value for a given key.

        The `key` parameter is a string
        """

        if not isinstance(key, str):
            raise Cache.GhostKeyError()
        else:
            request_object = CacheRequest(key)

            node = self.ring.get_point_for(key)
            
            if node == None:
                raise Cache.GhostNoMoreServersError()
                
            try:
                address = self.protocol + node.node + ":" + self.port + Cache._API_ENDPOINT_MAP["get"]
                json_obj = Cache.to_dict(request_object)
                headers = {'Content-type': 'application/json'}
                response = requests.post(address, headers=headers, data=json.dumps(json_obj))
                cache_response_obj = Cache.get_object_from_response_stream(response.text)
                return cache_response_obj
            except:
                Cache._DEAD_SERVERS.append(node.node)
                self.ring.delete(node.node)
                return self.get(key)


    def put(self, key, value, ttl=-1):
        """
        The `put()` method will add a key/value pair into the 
        cache. If the `key` already exists in the cache, it's value
        will be overwritten.

        The `key` parameter must be a string

        The `value` parameter can be of whatever type you want as 
        long as it is JSON serializable.

        If the key/value pair is successully added, the `STORED`
        message will be returned. Otherwise the `NOT_STORED` message
        will be returned.
        """

        if not isinstance(key, str):
            raise Cache.GhostKeyError()
        else:
            request_object = CacheRequest(key, value, ttl)
            node = self.ring.get_point_for(key)

            if node == None:
                raise Cache.GhostNoMoreServersError()

            try:
                address = self.protocol + node.node + ":" + self.port + Cache._API_ENDPOINT_MAP["put"]
                json_obj = Cache.to_dict(request_object)
                headers = {'Content-type': 'application/json'}
                response = requests.post(address, headers=headers, data=json.dumps(json_obj))
                cache_response_obj = Cache.get_object_from_response_stream(response.text)
                return cache_response_obj
            except Exception as e:
                print(str(e))
                Cache._DEAD_SERVERS.append(node.node)
                self.ring.delete(node.node)
                return self.put(key, value)

    def add(self, key, value, ttl=-1):
        """
        The `add()` method will add a key/value pair into the
        cache only if the `key` does not pre-exist in the cache.

        The `key` parameter must be a string

        The `value` parameter can be of whatever type you want
        as long as it is JSON serializable

        If the key/value pair is successully added, the `STORED`
        message will be returned. Otherwise the `NOT_STORED` message
        will be returned.
        """

        if not isinstance(key, str):
            raise Cache.GhostKeyError()
        else:
            request_object = CacheRequest(key, value, ttl)

            node = self.ring.get_point_for(key)

            if node == None:
                raise Cache.GhostNoMoreServersError()

            try:
                address = self.protocol + node.node + ":" + self.port + Cache._API_ENDPOINT_MAP["add"]
                json_obj = Cache.to_dict(request_object)
                headers = {'Content-type': 'application/json'}
                response = requests.post(address, headers=headers, data=json.dumps(json_obj))
                cache_response_obj = Cache.get_object_from_response_stream(response.text)
                return cache_response_obj
            except:
                Cache._DEAD_SERVERS.append(node.node)
                self.ring.delete(node.node)
                return self.add(key, value)

    def delete(self, key):
        """
        The `delete()` method will remove a key/value pair
        from the cache specified by the `key` parameter

        The `key` parameter must be a string

        If the key/value pair is successfully deleted, 
        the `REMOVED` message will be returned, otherwise
        the `NOT_FOUND` message will be returned
        """
        
        if not isinstance(key, str):
            raise Cache.GhostKeyError()
        else:
            request_object = CacheRequest(key)

            node = self.ring.get_point_for(key)

            if node == None:
                raise Cache.GhostNoMoreServersError()

            try:
                address = self.protocol + node.node + ":" + self.port + Cache._API_ENDPOINT_MAP["delete"]
                json_obj = Cache.to_dict(request_object)
                headers = {'Content-type': 'application/json'}
                response = requests.post(address, headers=headers, data=json.dumps(json_obj))
                cache_response_obj = Cache.get_object_from_response_stream(response.text)
                return cache_response_obj
            except:
                Cache._DEAD_SERVERS.append(node.node)
                self.ring.delete(node.node)
                return self.delete(node.node)

    def nodeSize(self, node):
        """
        The `nodeSize()` method will return the number
        of key/value pairs in a given node.
        """
        request_object = CacheRequest()
        nodes = self.ring.get_points()
        for n in nodes:
            print("NODE", node)
            print("N", n.node)
            if node == n.node:
                try:
                    address = self.protocol + n.node + ":" + self.port + Cache._API_ENDPOINT_MAP["nodeSize"]
                    json_obj = Cache.to_dict(request_object)
                    headers = {'Content-type': 'application/json'}
                    response = requests.post(address, headers=headers, data=json.dumps(json_obj))
                    cache_response_obj = Cache.get_object_from_response_stream(response.text)
                    return cache_response_obj
                except Exception as e:
                    Cache._DEAD_SERVERS.append(n.node)
                    self.ring.delete(n.node)
                    return None
        return None

    def flush(self, result=None, visitedNodes=None):
        """
        The `flush()` method will delete all key/value
        pairs from all nodes specified in the `node_file`
        at the time of flushing.
        """
        request_object = CacheRequest()

        if result is None:
            result = []

        if visitedNodes is None:
            visitedNodes = []

        nodes = self.ring.get_points()
        
        for node in nodes:
            try:
                if node.node not in visitedNodes:
                    address = self.protocol + node.node + ":" + self.port + Cache._API_ENDPOINT_MAP["flush"]
                    json_obj = Cache.to_dict(request_object)
                    headers = {'Content-type': 'application/json'}
                    response = requests.post(address, headers=headers, data=json.dumps(json_obj))
                    cache_response_obj = Cache.get_object_from_response_stream(response.text)
                    result.append({"node": node.node, "response": cache_response_obj})
                    visitedNodes.append(node.node)
            except:
                Cache._DEAD_SERVERS.append(node.node)
                self.ring.delete(node.node)
                return self.flush()

    def getSnitchMetrics(self, metrics=None, visitedNodes=None):
        """
        The `getSnitchMetrics()` method will fetch all
        snitch metricsfrom all nodes specified in the
        `node_file` at the time of calling.
        """
        if metrics is None:
            metrics = []
        
        if visitedNodes is None:
            visitedNodes = []

        nodes = self.ring.get_points()
        
        request_object = CacheRequest()

        for node in nodes:
            try:
                if node.node not in visitedNodes:
                    address = self.protocol + node.node + ":" + self.port + Cache._API_ENDPOINT_MAP["getSnitchMetrics"]
                    json_obj = Cache.to_dict(request_object)
                    headers = {'Content-type': 'application/json'}
                    response = requests.post(address, headers=headers, data=json.dumps(json_obj))
                    cache_response_obj = Cache.get_object_from_response_stream(response.text)
                    metrics.append({"node": node.node, "metrics": cache_response_obj})
                    visitedNodes.append(node.node)
            except Exception as e:
                Cache._DEAD_SERVERS.append(node.node)
                self.ring.delete(node.node)
                return self.getSnitchMetrics(metrics, visitedNodes)
        return metrics
    
    def getWatchdogMetrics(self, metrics=None, visitedNodes=None):
        """
        The `getWatchdogMetrics()` method will fetch all
        application metrics from all nodes specified in the
        `node_file` at the time of calling.
        """
        if metrics is None:
            metrics = []
        
        if visitedNodes is None:
            visitedNodes = []

        nodes = self.ring.get_points()

        request_object = CacheRequest()
        
        for node in nodes:
            try:
                if node.node not in visitedNodes:
                    address = self.protocol + node.node + ":" + self.port + Cache._API_ENDPOINT_MAP["getWatchdogMetrics"]
                    json_obj = Cache.to_dict(request_object)
                    headers = {'Content-type': 'application/json'}
                    response = requests.post(address, headers=headers, data=json.dumps(json_obj))
                    cache_response_obj = Cache.get_object_from_response_stream(response.text)
                    metrics.append({"node": node.node, "metrics": cache_response_obj})
                    visitedNodes.append(node.node)
            except:
                Cache._DEAD_SERVERS.append(node.node)
                self.ring.delete(node.node)
                return self.getWatchdogMetrics(metrics, visitedNodes)
        return metrics

    def ping(self, liveNodes=None, visitedNodes=None):

        if liveNodes == None:
            liveNodes = []
        
        if visitedNodes == None:
            visitedNodes = []

        request_object = CacheRequest()

        nodes = self.ring.get_points()
        for node in nodes:
            try:
                if node.node not in visitedNodes:
                    address = self.protocol + node.node + ":" + self.port + Cache._API_ENDPOINT_MAP["ping"]
                    json_obj = Cache.to_dict(request_object)
                    headers = {'Content-type': 'application/json'}
                    response = requests.post(address, headers=headers, data=json.dumps(json_obj))
                    if response.status_code == 200:
                        liveNodes.append(node.node)
                    visitedNodes.append(node.node)
            except:
                Cache._DEAD_SERVERS.append(node.node)
                self.ring.delete(node.node)
                return self.ping(liveNodes, visitedNodes)
        return liveNodes

    def _server_revive(self):
        for i, server in enumerate(Cache._DEAD_SERVERS):
            try:
                address = self.protocol + server + ":" + self.port + Cache._API_ENDPOINT_MAP["ping"]
                response = requests.get(address)
                if response.status_code == 200:
                    self.ring.add(server)
                    Cache._DEAD_SERVERS.pop(i)
            except Exception as e:
                continue
        threading.Timer(Cache._REVIVE_WAIT, self._server_revive).start()

    def _default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)

    @staticmethod
    def get_object_from_response_stream(stream):
        return cache_response_json_decoder(stream)

    @staticmethod
    def to_dict(obj):
        return json.loads(json.dumps(obj, default=lambda o: o.__dict__))