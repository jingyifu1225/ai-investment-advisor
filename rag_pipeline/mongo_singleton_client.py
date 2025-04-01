from typing import Optional
import threading
import certifi
from pymongo import MongoClient


class MongoDBClient:
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def get_instance(cls, connection_string=None):
        if cls._instance is None:
            if connection_string is None:
                from django.conf import settings
                connection_string = settings.MONGO_URI
            try:
                client = MongoClient(
                    connection_string,
                    serverSelectionTimeoutMS=10000,
                    tlsCAFile=certifi.where()
                )

                client.admin.command('ping')
                print("MongoDB succeeds!")

                cls._instance = client
            except Exception as e:
                print(f"MongoDB failed: {e}")
                return None

        return cls._instance
