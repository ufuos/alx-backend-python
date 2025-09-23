import logging
from datetime import datetime
from datetime import datetime
from django.http import HttpResponseForbidden
import time
from django.http import JsonResponse
from collections import defaultdict, deque
from django.http import JsonResponse

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Dictionary to track IP → deque of timestamps
        self.ip_message_log = defaultdict(lambda: deque())

        # Limit settings
        self.limit = 5  # max messages
        self.time_window = 60  # seconds (1 minute)

    def __call__(self, request):
        # Only track chat messages (POST requests)
        if request.method == "POST":
            # Get user IP address
            ip_address = self.get_client_ip(request)

            # Get current time
            now = time.time()

            # Get message history for this IP
            message_times = self.ip_message_log[ip_address]

            # Remove timestamps older than 60 seconds
            while message_times and now - message_times[0] > self.time_window:
                message_times.popleft()

            # If user has already reached the limit
            if len(message_times) >= self.limit:
                return JsonResponse(
                    {"error": "Rate limit exceeded. Try again later."},
                    status=429,
                )

            # Record this message timestamp
            message_times.append(now)

        # Continue processing the request
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Helper method to extract client IP address"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "")
    
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
