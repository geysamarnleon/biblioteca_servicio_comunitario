from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.views.generic.edit import FormView
from django.contrib import messages
from .forms import RecoverPassword
# Create your views here.
User = get_user_model()








class LogoutView(FormView):
    def get(self, request, *args, **kwargs):
        messages.info(request, "Vuelva pronto.")
        logout(request)
        return redirect("main:home")


