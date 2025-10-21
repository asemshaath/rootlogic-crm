from django.http import JsonResponse, Http404
from django.urls import Resolver404

class JSONErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except (Http404, Resolver404):
            return JsonResponse({'error': True, 'message': 'Not found'}, status=404)
        except Exception as exc:
            return JsonResponse({'error': True, 'message': str(exc)}, status=500)
