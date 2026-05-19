FREE_DAILY_LIMIT = 20

user_limits = {}


def can_use_free(user_id):

    count = user_limits.get(user_id, 0)

    if count >= FREE_DAILY_LIMIT:
        return False

    user_limits[user_id] = count + 1

    return True
