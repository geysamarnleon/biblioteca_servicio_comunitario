from django import forms
from .models import AuthUser
from django.contrib.auth import get_user_model
from django.contrib import messages
User = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'Ingrese su email'}) )
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
        'class':'form-control',
        'placeholder':'*********'
        }
    ))


class RecoverPassword(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'Inserte su correo'}) )

    def clean(self):
        cleaned = super().clean()
        if not User.objects.filter(email=cleaned['email']).exists():
            
            raise forms.ValidationError('El usuario no existe')
        return cleaned

    def get_user(self):
        email = self.cleaned_data.get('email')
        return User.objects.get(email=email)

    # forms.PasswordInput

    # class Meta:
    #     model = AuthUser
    #     fields = ['email', 'password']
    #     widgets = {
    #         'email': forms.EmailField(attrs={'placeholder' : 'Escribe tu correo'}),
    #         'password': forms.PasswordInput(attrs={'placeholder' : 'Escribe tu correo'})
    #     }


class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Inserte su contraseña'}) )
    

    confirmpassword = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Repita la contraseña'}) )
    
    def clean(self):
        cleaned = super().clean()
        print(cleaned)
        password = cleaned['password']
        confirmpassword = cleaned['confirmpassword']
        if password!=confirmpassword:
            raise forms.ValidationError('Las contraseñas no son iguales')
        return cleaned
