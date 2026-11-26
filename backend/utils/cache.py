# """
# Redis cache utilities for Vehicle Parking App V2.
# """
#     """Cache data in Redis with an expiry (in seconds)."""
#     if current_app and hasattr(current_app, 'redis') and current_app.redis:
#         current_app.redis.setex(key, expiry, json.dumps(data))

# def get_cached_data(key):
#     """Retrieve cached data from Redis."""
#     """Delete all Redis keys matching the given pattern."""
#     if current_app and hasattr(current_app, 'redis') and current_app.redis:
#         for key in current_app.redis.scan_iter(key_pattern):
#             current_app.redis.delete(key)
