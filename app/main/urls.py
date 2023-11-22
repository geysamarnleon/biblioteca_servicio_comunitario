from django.urls import path
from .views import IndexView, DocumentDetailView

app_name = "main"
urlpatterns = [
    path("", IndexView.as_view(), name="home"),
    path("view/<str:id>/", DocumentDetailView.as_view(), name="document"),
]
