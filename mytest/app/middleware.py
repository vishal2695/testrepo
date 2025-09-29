# myapp/middleware.py
import logging
import time

logger = logging.getLogger("django.request")

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        duration = round(time.time() - start_time, 4)
        method = request.method
        path = request.get_full_path()
        status = response.status_code
        ip = request.META.get("REMOTE_ADDR")

        logger.info(
            f"{method} {path} | Status: {status} | Duration: {duration}s | IP: {ip}"
        )

        return response
