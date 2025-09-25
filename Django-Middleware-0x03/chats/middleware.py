import datetime
class RequestLoggingMiddleware:
    """Middleware to log incoming requests with specific format"""
    def __init__(self, get_response):
        """Store the get_response callable to call it later(next middleware)"""
        self.get_response = get_response

    def __call__(self, request):
        with open("requests.log", mode="w", encoding="utf-8") as f:
            f.write(f'{datetime.datetime.now()} - User: {request.user} - Path: {request.path}\n')
            return self.get_response(request)