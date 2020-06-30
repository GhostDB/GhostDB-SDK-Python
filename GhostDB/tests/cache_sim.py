"""
THIS SCRIPT SIMULATES SERVERS GOING OFFLINE AND ONLINE AGAIN

BASIC SIMULATION:
    - INITIALLY START WITH ALL SERVERS OFFLINE
    - RUN THIS SCRIPT
    - BRING A SERVER ONLINE
    - SCRIPT SHOULD REVIVE ONLINE SERVERS BEFORE SLEEP OF 45 SECONDS IS UP
    - BRING THAT SERVER DOWN AND ANOTHER UP

KEYSPACE TRANSFER SIMULATION:
    - START WITH ONE SERVER ONLINE AND THE OTHER OFFLINE
    - SET A KEY/VALUE PAIR - THIS WILL GO TO THE ONLINE SERVER
    - BRING THE LIVE SERVER DOWN AND THE OFFLINE SERVER ONLINE
    - SET THE VALUE AGAIN - THE KEY SHOULD BE SET ON THE NEW LIVE SERVER
"""

from GhostDB import cache
import time

cache = cache.Cache("ghostdb_sim.conf")


def cache_data(key, value):
    try:
        print("PUT VALUE: " + value + " FOR KEY: " + key)
        resp = cache.put(key, value)
        return resp
    except cache.GhostNoMoreServersError as e:
        print(e)
        return None

def add_data(key, value):
    try:
        print("ADD VALUE: " + value + " FOR KEY: " + key)
        resp = cache.add(key, value)
        return resp
    except cache.GhostNoMoreServersError as e:
        print(e)
        return None

def delete_data(key):
    try:
        print("DELETE KEY: " + key)
        resp = cache.delete(key)
        return resp
    except cache.GhostNoMoreServersError as e:
        print(e)
        return None

def flush_cache():
    try:
        print("FLUSHING CACHE")
        resp = cache.flush()
        return resp
    except cache.GhostNoMoreServersError as e:
        print(e)
        return None

def get_stats():
    try:
        print("GETTING SNITCH METRICS")
        resp = cache.getSnitchMetrics()
        return resp
    except cache.GhostNoMoreServersError as e:
        print(e)
        return None

def get_watchdog():
    try:
        print("GETTING WATCHDOG METRICS")
        resp = cache.getWatchdogMetrics()
        return resp
    except cache.GhostNoMoreServersError as e:
        print(e)
        return None

def get_data(key):
    try:
        print("GETTING DATA")
        resp = cache.get(key)
        return resp
    except cache.GhostNoMoreServersError as e:
        print(e)
        return None

def get_size(node):
    try:
        print("GETTING SIZE")
        resp = cache.nodeSize(node)
        return resp
    except cache.GhostNoMoreServersError as e:
        print(e)
        return None


def main():  
    i = 0
    while i < 2:
        res = cache_data("Dublin", "Ireland")
        print("PUT", res)
        res = get_data("Dublin")
        print("GET", res)
        res = add_data("Dublin", "Irealnd")
        print("ADD", res)
        # res = delete_data("Dublin")
        # print(res)
        res = cache_data("Italy", "Rome")
        print("PUT", res)
        # res = get_data("Italy")
        # print("GET", res)
        # res = flush_cache()
        # print("FLUSH", res)
        # res = get_data("Italy")
        # print("GET", res)
        # res = get_stats()
        # print("STATS", res)
        res = get_size("127.0.0.1")
        print("SIZE", res)
        time.sleep(45)

if __name__ == "__main__":
    main()