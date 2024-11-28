import logging

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
        # Log the request method and path
        self.logger.info(f"Request Method: {request.method}, Path: {request.path}")

        # Get the response
        response = self.get_response(request)

        return response