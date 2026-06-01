from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("api/match/", views.MatchCreateView.as_view(), name="match-create"),
    path("api/match/<int:pk>/", views.MatchDetailView.as_view(), name="match-detail"),
    path("api/matches/", views.MatchListView.as_view(), name="match-list"),
]
