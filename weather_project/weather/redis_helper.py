from django_redis import get_redis_connection


def increment_city_search_count(city):
    """
        Increases the search query count for the specified city in Redis.

        The key structure:
    - "city_search_counts": Sorted Set, members are cities, values are number of queries.
    """
    redis_conn = get_redis_connection("default")
    redis_conn.zincrby("city_search_counts", 1, city)


def get_top_cities(limit=10):
    """
       Gets a list of the most popular cities based on the number of search queries.

        Arguments:
        limit (int): Maximum number of cities returned (default is 10).

        The key structure:
    - "city_search_counts": Sorted Set, returns (city, number of requests).
    """
    redis_conn = get_redis_connection("default")
    return redis_conn.zrevrange("city_search_counts", 0, limit - 1, withscores=True)
