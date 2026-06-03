from django.http import JsonResponse
from django.urls import path


def health(_request):
    return JsonResponse({"status": "ok", "app": "resumatch"})


def root(_request):
    return JsonResponse({"app": "resumatch", "message": "Hello from Harbor 👋"})


urlpatterns = [
    path("health", health),
    path("", root),
]
