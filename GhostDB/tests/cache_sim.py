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

def main():  
    i = 0
    while i < 2:
        res = cache_data("Dublin", "Ireland")
        print(res)
        time.sleep(45)

if __name__ == "__main__":
    main()