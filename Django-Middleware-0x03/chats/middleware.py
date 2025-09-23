import logging
from datetime import datetime

# Configure logging: log to requests.log file
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("requests.log")
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


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
