from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.views import View

from biblioteca_SC.utils.driver_connection import get_id_from_url
from biblioteca_SC.models import Project_SC
from authentication.forms import LoginForm
from .forms import FilterForm


class IndexView(View):
    form_login = LoginForm
    form_filter1 = FilterForm
    form_filter2 = None
    row_for_page = 3

    template_name = "index.main.html"
    model = Project_SC

    def get_projects(self, request, is_project=None):
        if not is_project:
            if_query = request.GET.get("filter")
            if if_query:
                proyectos_list = Project_SC.objects.filter(
                    Q(titulo__icontains=if_query)
                    | Q(ubicacion_servicio__icontains=if_query)
                    | Q(tematica__icontains=if_query)
                    | Q(periodo__icontains=if_query)
                )
            else:
                proyectos_list = self.model.objects.get_queryset().order_by("periodo")
            paginator = Paginator(proyectos_list, self.row_for_page)
        else:
            paginator = Paginator(is_project, self.row_for_page)

        pagina = request.GET.get("pagina")
        return paginator.get_page(pagina)

    def get(self, request, *args, **kwargs):
        context = {}

        proyectos = self.get_projects(request)
        context["proyectos"] = proyectos

        if request.GET.get("next"):
            messages.warning(request, "No se puede acceder, por favor inicie sesión para ver si tiene acceso.")
            context["showFormLogin"] = "show"

        form_filter1 = self.form_filter1()
        form_login = self.form_login()

        if_query = request.GET.get("filter")
        print("➡ if_query :", if_query)

        context["form_login"] = form_login
        context["filter_query"] = if_query
        context["form_filter1"] = form_filter1
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        context = {}

        form_login = self.form_login(request.POST)
        form_filter1 = self.form_filter1(request.POST)
        context["form_login"] = form_login
        context["form_filter1"] = form_filter1
        proyectos = self.get_projects(request)

        print("➡ form_filter1 :", form_filter1.errors)
        if form_filter1.is_valid():
            data = form_filter1.cleaned_data
            print("➡ data :", data)
            proyectos_area = self.model.objects.filter(Q(area__in=data["areas"]) | Q(programa__in=data["programas"]))
            print("➡ proyectos_area :", proyectos_area)
            proyectos = self.get_projects(request, proyectos_area)

        if form_login.is_valid():
            data = form_login.cleaned_data
            user = authenticate(email=data["email"], password=data["password"])
            if user:
                messages.info(request, "Inicio de sesión exitoso")
                login(request, user)
                return redirect("main:home")
            else:
                messages.error(request, "Correo o contraseña incorrecta")

        context["proyectos"] = proyectos
        return render(request, self.template_name, context=context)


class DocumentDetailView(View):
    form_login = LoginForm
    model = Project_SC
    template_name = "document-details.main.html"

    def get(self, request, *args, **kwargs):
        print("➡ kwargs :", kwargs)
        form_login = self.form_login()

        proyecto = self.model.objects.get(id=kwargs["id"])
        try:
            id_file = get_id_from_url(proyecto.file.url)
            file_url = f"https://drive.google.com/file/d/{id_file}/preview"
        except:
            file_url = None

        context = {"form_login": form_login, "proyecto": proyecto, "file_url": file_url}
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        context = {}

        form_login = self.form_login(request.POST)

        if form_login.is_valid():
            data = form_login.cleaned_data
            user = authenticate(email=data["email"], password=data["password"])
            if user:
                messages.info(request, "Inicio de sesión exitoso")
                login(request, user)
                return redirect("main:home")
            else:
                messages.error(request, "Correo o contraseña incorrecta")

        return redirect("main:document")
