import django.forms as forms
from authentication.models import Area, Programa


class FilterForm(forms.Form):
    areas = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Area.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    programas = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Programa.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
