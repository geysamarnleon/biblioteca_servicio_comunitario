from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *


app_name = "authentication"
urlpatterns = [
    path("logout/", LogoutView.as_view(), name="logout"),
]
