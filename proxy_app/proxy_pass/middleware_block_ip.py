from django.http import HttpResponseForbidden
from django.conf import settings
import logging

logger = logging.getLogger("django")


class BlockIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = request.META.get("REMOTE_ADDR")
        logger.info(f"== Meta remote addr {ip_address} ==")
        if ip_address in settings.BLOCKED_IPS:
            response = HttpResponseForbidden("Raise middleware IP block.")
            response.status_code = 403
            return response
        return self.get_response(request)
