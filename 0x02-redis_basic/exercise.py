#!/usr/bin/env python3
""" using redis """
import redis
from typing import Union
import uuid


class Cache:
    """
    A class that represents a cache using Redis.

    Attributes:
        _redis (redis.Redis): The Redis client object.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the Cache class.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the given data in the cache.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored.

        Returns:
            str: The generated key for the stored data.
        """
        rkey = str(uuid.uuid4())
        self._redis.set(rkey, data)
        return rkey
