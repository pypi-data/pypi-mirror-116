"""Requests module."""

from functools import wraps
import json
from typing import Callable

from flask import current_app, request
from werkzeug.exceptions import TooManyRequests
from redis import Redis

from notelist.config import sm
from notelist.tools import get_current_ts
from notelist.responses import ResponseData


# Requests Redis database client. By not setting "decode_responses" to True
# (the default value is False), calls to "requests_redis.get" will return bytes
# instead of a string value.
requests_redis = Redis(
    sm.get("NOTELIST_REDIS_HOST"),
    sm.get("NOTELIST_REDIS_PORT"),
    sm.get("NOTELIST_REDIS_REQUESTS_DB"),
    sm.get("NOTELIST_REDIS_PASSWORD"))


def req_limit(min_sec: int) -> Callable:
    """Limit the number of requests per client, URL and method.

    This is a decorator for view functions. If a client (based on its address)
    makes a request to a given URL and method and then makes a second request
    to the same URL and method less than `min_sec` seconds later, a HTTP 429
    error (Too Many Requests) response is returned.

    :param sec: Minimum number of seconds to wait between one request and
    another.
    """
    def wrapper1(f: Callable) -> Callable:
        @wraps(f)
        def wrapper2(*args, **kwargs) -> ResponseData:
            # If we are running tests, then we don't apply the limit
            if current_app.config.get("TESTING"):
                return f(*args, **kwargs)

            # Request data
            req = {
                "client_address": request.remote_addr,
                "url": request.url,
                "method": request.method}

            # Get existing request if it exists
            req_id = json.dumps(req, sort_keys=True)
            req_ts = requests_redis.get(req_id)  # It returns bytes or None

            # Save request
            current_ts = get_current_ts()
            requests_redis.set(req_id, current_ts, ex=min_sec)

            # If the request exists, calculate the time difference between the
            # current time and the request time (in seconds) and raise an
            # exception if the time difference is lower than "min_sec".
            if req_ts is not None and (current_ts - int(req_ts)) < min_sec:
                raise TooManyRequests(retry_after=min_sec)

            # Call decorated function and return its returned value
            return f(*args, **kwargs)

        return wrapper2

    return wrapper1
