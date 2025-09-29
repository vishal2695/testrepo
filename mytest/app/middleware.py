# myapp/middleware.py
import logging
import time
import json

logger = logging.getLogger("django.request")

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        try:
            response = self.get_response(request)
            status = "SUCCESS" if 200 <= response.status_code < 400 else "FAILED"
        except Exception as e:
            response = None
            status = "FAILED"
            logger.exception(f"Unhandled exception: {e}")
            raise

        duration = round(time.time() - start_time, 4)
        ip = request.META.get("REMOTE_ADDR")
        method = request.method
        path = request.get_full_path()

        # capture request body safely (only JSON / form)
        try:
            if request.body:
                body_data = request.body.decode("utf-8")
                body_data = json.loads(body_data) if "application/json" in request.content_type else body_data
            else:
                body_data = None
        except Exception:
            body_data = "<unreadable>"

        log_data = {
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "ip": ip,
            "method": method,
            "path": path,
            "status": status,
            "http_status": response.status_code if response else 500,
            "duration": f"{duration}s",
            "request_data": body_data,
        }

        logger.info(json.dumps(log_data))  # store as JSON line

        return response
