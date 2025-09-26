import datetime
from django.http import HttpResponseForbidden
class RequestLoggingMiddleware:
    """Middleware to log incoming requests with specific format"""
    def __init__(self, get_response):
        """Store the get_response callable to call it later(next middleware)"""
        self.get_response = get_response

    def __call__(self, request):
        with open("requests.log", mode="w", encoding="utf-8") as f:
            f.write(f'{datetime.datetime.now()} - User: {request.user} - Path: {request.path}\n')
            return self.get_response(request)

class RestrictAccessByTimeMiddleware:
    """Middleware to restrict access to the messaging up during specific time"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = datetime.time(18, 00)
        end_time = datetime.time(21,00)
        current_time = datetime.datetime.now().time()

        if start_time <= current_time <= end_time:
            return HttpResponseForbidden("access is denied between between 18:00 and 21:00")

        return self.get_response(request)

class OffensiveLanguageMiddleware:
    """Middleware to prevent sending 5 messages in ore than 5 minutes"""
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_message_dict = {}

    def __call__(self, request):
        if request.method == 'POST' and request.path == 'messages':
            ip = request.META.get('REMOTE_ADDR')
            now = datetime.datetime.now()
            one_min_ago = now - datetime.timedelta(min=1)
            timestamps = self.ip_message_dict.get(ip, [])
            timestamps = [timestamp for timestamp in timestamps if timestamp > one_min_ago]
            if len(timestamps) >= 5:
                return HttpResponseForbidden("you exceeded message limit")
            timestamps.append(now)
            self.ip_message_dict['ip'] = timestamps
        return self.get_response


class RolepermissionMiddleware:
    """"Middleware checks the user’s role i.e admin, before allowing access to specific actions"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return HttpResponseForbidden("authentication required")

        if user.role != 'admin':
            return HttpResponseForbidden("you are not admin")
        return self.get_response(request)

