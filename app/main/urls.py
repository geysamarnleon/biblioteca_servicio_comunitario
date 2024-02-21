
from django.urls import reverse_lazy
from django.urls import path


from .views import IndexView, DocumentDetailView,  RecoverPasswordView, ChangePasswordView

app_name = "main"
urlpatterns = [

    path("", IndexView.as_view(), name="home"),
    path("view/<str:id>/", DocumentDetailView.as_view(), name="document"),
    path("recoverpassword/", RecoverPasswordView.as_view(), name="reset_password"),
    path("changepassword/<str:token>/", ChangePasswordView.as_view(), name="change_password"),
]
