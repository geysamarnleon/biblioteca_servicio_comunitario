from django.urls import path
from .views import EditProjectView, RegisterProjectView, DeleteProjectView

app_name = "biblioteca"
urlpatterns = [
    path("register/", RegisterProjectView.as_view(), name="register-project"),
    path("register/<str:id>", RegisterProjectView.as_view(), name="register-project-edit"),
    path("edit/", EditProjectView.as_view(), name="edit-project"),
    path("delete/", DeleteProjectView.as_view(), name="delete-project"),
]
