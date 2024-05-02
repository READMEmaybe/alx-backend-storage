#!/usr/bin/env python3
""" using redis """
import redis
from typing import Union, Optional, Callable
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    A decorator that counts the number of times a function has been called.

    Args:
        method (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    A decorator that stores the history of inputs and outputs for a function.

    Args:
        method (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.rpush(method.__qualname__ + ":inputs", str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(method.__qualname__ + ":outputs", str(result))
        return result
    return wrapper


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

    @call_history
    @count_calls
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

    def get(self, key: str, fn: Optional[Callable] = None
            ) -> Union[str, bytes, int, float]:
        """
        Retrieves the value associated with the given key from the cache.

        Args:
            key (str): The key to retrieve the value for.
            fn (Optional[Callable]):
                    An optional function to apply to the retrieved value.

        Returns:
            Union[str, bytes, int, float]: The retrieved value
        """
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """
        Retrieves the string value associated with the given key from the cache

        Args:
            key (str): The key to retrieve the string value for.

        Returns:
            str: The retrieved string value.
        """
        return self.get(key, fn=str)

    def get_int(self, key: str) -> int:
        """
        Retrieves the int value associated with the given key from the cache.

        Args:
            key (str): The key to retrieve the integer value for.

        Returns:
            int: The retrieved integer value.
        """
        return self.get(key, fn=int)
