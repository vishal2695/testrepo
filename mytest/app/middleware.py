import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('django_request')  # Use a separate logger for requests

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = getattr(request, 'user', None)
        user_str = user.username if user and user.is_authenticated else 'Anonymous'
        ip = self.get_client_ip(request)

        logger.info(
            f"User: {user_str} | "
            f"Method: {request.method} | "
            f"Path: {request.get_full_path()} | "
            f"IP: {ip}"
        )

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip