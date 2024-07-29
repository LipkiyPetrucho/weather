from django_redis import get_redis_connection


def increment_city_search_count(city):
    redis_conn = get_redis_connection("default")
    redis_conn.zincrby("city_search_counts", 1, city)

def get_top_cities(limit=10):
    redis_conn = get_redis_connection("default")
    return redis_conn.zrevrange("city_search_counts", 0, limit - 1, withscores=True)