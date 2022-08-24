import parallel_requests
from django.core.cache import cache
from config.consts import *


def parallel_get_with_cache(urls, key):
    response_list = []
    not_cached_urls = []

    for url in urls:
        # Get the cached response for this url
        cached_response = cache.get(url)
        if cached_response:
            # If cache is present, use the cache response
            response_list += cached_response[key]
        else:
            # If there is no cache, call the url below
            not_cached_urls.append({'url': url})

    # If cache is present for all urls, return the response
    if len(not_cached_urls) == 0:
        return response_list

    # Call urls simultaneously
    responses: parallel_requests.ListResponse = parallel_requests.get(
        method_args=not_cached_urls,
        max_workers=10,
    )
    for index, response in enumerate(responses):
        if response.status_code != 200:
            return False
        # Save the response in cache
        cache.set(not_cached_urls[index]['url'], response.json(), timeout=REDIS_CACHE_TIMEOUT_POSTS)
        response_json = response.json()
        response_list += response_json[key]

    return response_list
