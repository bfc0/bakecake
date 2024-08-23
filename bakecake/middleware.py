from django.utils.deprecation import MiddlewareMixin
from cakes.models import Visit


class VisitMiddleware(MiddlewareMixin):
    def process_request(self, request):
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
        session_key = request.session.session_key
        user = request.user if request.user.is_authenticated else None
        Visit.objects.create(user=user, session_key=session_key)
