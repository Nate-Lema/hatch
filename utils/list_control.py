import operator


def remove_duplicate(items):
    item_dic = {}
    for item in items:
        # Push items with id keys, we can then remove the same ids.
        item_dic[item['id']] = item

    new_items = []
    for key, value in item_dic.items():
        # Revert the format from dictionary to list
        new_items.append(value)

    return new_items


def sort_response(posts, sort_by, direction):
    if sort_by == '':
        return posts

    if direction == '':
        direction = 'asc'

    dic = {}
    for post in posts:
        dic[post['id']] = post[sort_by]

    sorted_list = sorted(dic.items(), key=operator.itemgetter(1))

    sorted_posts = []
    for value in sorted_list:
        postId = value[0]
        for post in posts:
            if post['id'] == postId:
                sorted_posts.append(post)

    if direction == 'desc':
        sorted_posts.reverse()

    return sorted_posts
