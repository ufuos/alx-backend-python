import logging
from datetime import datetime
from datetime import datetime
from django.http import HttpResponseForbidden

# Configure logging: log to requests.log file
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("requests.log")
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict chat access based on server time.
    Allowed access window: 6PM (18:00) to 9PM (21:00).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the current server hour
        current_hour = datetime.now().hour

        # Restrict access if outside allowed time
        if not (18 <= current_hour < 21):  # Only between 18:00 and 20:59
            return HttpResponseForbidden(
                "⛔ Chat access restricted: Available only between 6PM and 9PM."
            )

        # Continue processing request


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        # Django calls this once when the server starts
        self.get_response = get_response

    def __call__(self, request):
        # Get user if authenticated, else "Anonymous"
        user = request.user if request.user.is_authenticated else "Anonymous"

        # Log the request details
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        # Continue processing the request
        response = self.get_response(request)
        return response
