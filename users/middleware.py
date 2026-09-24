from datetime import datetime
from pathlib import Path


class RequestLoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        ip = request.META.get("REMOTE_ADDR", "Unknown")

        response = self.get_response(request)

        log_file = Path(__file__).resolve().parent.parent / "requests.txt"

        with open(log_file, "a") as file:
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