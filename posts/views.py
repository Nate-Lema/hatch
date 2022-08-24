from django.http import JsonResponse
from config.consts import *
from utils.parallel_requests import parallel_get_with_cache
from utils.list_control import remove_duplicate, sort_response


def postListView(request):
    # ---------------------
    # Check parameters
    # ---------------------

    tags = request.GET.get('tags', None)
    if tags is None or tags == '':
        return JsonResponse(status=400, data={'error': 'Tags parameter is required'})

    sort_by = request.GET.get('sortBy', '')
    if sort_by != '' and sort_by not in ['id', 'reads', 'likes', 'popularity']:
        return JsonResponse(status=400, data={'error': 'sortBy parameter is invalid'})

    direction = request.GET.get('direction', '')
    if direction != '' and direction not in ['desc', 'asc']:
        return JsonResponse(status=400, data={'error': 'direction parameter is invalid'})

    # ---------------------
    # Call API simultaneously
    # ---------------------
    tags = tags.split(',')
    posts = []
    urls = []
    base_url = HATCHWAYS_API_URL + '?tag='

    for tag in tags:
        urls.append(base_url + tag)

    # Call API simultaneously, and to quicken the response, save them to cache.
    posts = parallel_get_with_cache(urls, 'posts')
    if posts == False:
        return JsonResponse(status=404, data={'error': 'Could not connect to external API'})

    # ---------------------
    # Clean up and Sort the response
    # ---------------------
    # Remove duplicate
    clean_posts = remove_duplicate(posts)

    # Sort posts
    sorted_posts = sort_response(clean_posts, sort_by, direction)

    return JsonResponse({'posts': sorted_posts})
