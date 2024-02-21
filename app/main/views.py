from core import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.views import View
from django.views.generic import FormView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from biblioteca_SC.utils.driver_connection import get_id_from_url
from biblioteca_SC.models import Project_SC
from authentication.forms import LoginForm, RecoverPassword, ChangePasswordForm, User
from .forms import FilterForm
from core import settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template.loader import render_to_string
import uuid



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
            messages.warning(request, "No se puede acceder, Inicie sesión para verificar qué tenga acceso.")
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

class RecoverPasswordView(FormView):
    form_class = RecoverPassword
    template_name = "reset_password.html"
    sucess_url = reverse_lazy('main:home')
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,*args,**kwargs)
    

    def send_email(self,user):
        data = {}
        try:
            URL = settings.DOMAIN if not settings.DEBUG else self.request.META['HTTP_HOST']
            user.token = uuid.uuid4()
            user.save()
            mailServer = smtplib.SMTP('smtp-mail.outlook.com',587)
            mailServer.ehlo()
            mailServer.starttls()
            mailServer.ehlo()
            mailServer.login('recoveraisunergpassword@outlook.com','132344xdd')
            email_to = user.email #Obtiene el correo electronico del registrado
            mensaje = MIMEMultipart()
            mensaje['From']="recoveraisunergpassword@outlook.com"
            mensaje['To']= email_to
            mensaje['Subject']="Reseteo de contraseña"
            content = render_to_string('password_reset_confirm.html',{
                'user':user,
                'link_resetpwd':'http://{}/changepassword/{}/'.format(URL,str(user.token)),
                'link_home':'http://{}'.format(URL)
                })
        
            mensaje.attach(MIMEText(content,'html'))
            mailServer.sendmail("recoveraisunergpassword@outlook.com",
                                email_to,
                                mensaje.as_string())
            print('Correo enviado correctamente')
        except Exception as e:
            data['error'] = str(e)
        return data

    def post(self, request, *args, **kwargs):
        data = {}
        try:
           

            form = RecoverPassword(request.POST)
            if form.is_valid():
                user = form.get_user()
                self.send_email(user)
                messages.info(request, "Email enviado correctamente")
                return redirect("main:reset_password")
            else:
                messages.error(request, "No se encuentra este correo")
                return redirect("main:reset_password")
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reseteo de contraseña'
        return context

class ChangePasswordView(FormView):
    form_class = ChangePasswordForm
    template_name = "reset_password_change.html"
    sucess_url = reverse_lazy('main:home')
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,*args,**kwargs)
    
    
    def get(self, request, *args, **kwargs):
        token = self.kwargs['token']
        if User.objects.filter(token=token).exists():
            return super().get(request,*args,**kwargs)
        return HttpResponseRedirect('/')
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = ChangePasswordForm(request.POST)
            print(form)
            if form.is_valid():
                user = User.objects.get(token=self.kwargs['token'])
                user.set_password(request.POST['password'])
                user.token = uuid.uuid4()
                user.save()
                messages.success(request, "Usted cambio su contraseña de manera correcta")
                return redirect("main:home")
            else:
                messages.error(request, "Las contraseñas no son iguales")
                return redirect("main:reset_password")
        except Exception as e:
            print(e)
            data['error'] = str(e)
        return JsonResponse(data,safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cambio de contraseña'
       




        return context
    

