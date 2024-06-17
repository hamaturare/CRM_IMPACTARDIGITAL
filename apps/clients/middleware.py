from django.utils.deprecation import MiddlewareMixin

class StorePrevURLMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if 'update_client' in request.path:
            request.session['prev_url'] = request.META.get('HTTP_REFERER', '/')
            #print(f"Previous URL stored in session: {request.session['prev_url']}")