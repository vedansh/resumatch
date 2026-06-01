from django.http import JsonResponse
from django.urls import include, path


def health(_request):
    return JsonResponse({"status": "ok", "app": "resumatch"})


urlpatterns = [
    path("health", health),
    path("", include("matcher.urls")),
]
