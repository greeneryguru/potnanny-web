from django.forms import ModelForm
from .models import Outlet

class OutletForm(ModelForm):
    class Meta:
        model = Outlet
        fields = ['name', 'channel']

