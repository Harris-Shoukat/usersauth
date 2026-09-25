from datetime import datetime
from pathlib import Path
from django.core.cache import cache
from django.http import JsonResponse


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "Unknown")


class RequestLoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = get_client_ip(request)

        response = self.get_response(request)

        log_file = Path(__file__).resolve().parent.parent / "requests.txt"

        with open(log_file, "a", encoding="utf-8") as file:
            file.write(
                "\n"
                + "=" * 50
                + "\n"
                + f"Time: {datetime.now()}\n"
                + f"IP: {ip}\n"
                + f"Method: {request.method}\n"
                + f"Path: {request.path}\n"
                + f"Status: {response.status_code}\n"
                + "=" * 50
                + "\n"
            )

        return response


class RateLimitMiddleware:

    MAX_REQUESTS = 5
    WINDOW = 60

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = get_client_ip(request)

        cache_key = f"rate_limit:{ip}"

        redis_client = cache.client.get_client()

        request_count = redis_client.incr(cache_key)

        if request_count == 1:
            redis_client.expire(cache_key, self.WINDOW)

        if request_count > self.MAX_REQUESTS:
            return JsonResponse(
                {"detail": "Too many requests. Try again after 1 minute."},
                status=429,
            )

        return self.get_response(request)
