from django import forms
from .models import Outlet

class OutletForm(forms.ModelForm):
    class Meta:
        model = Outlet
        fields = ['name', 'channel']
        widgets = {
            'name': forms.TextInput(attrs={
                                        'required': True,
                                        'class': 'form-control' }),
            'channel': forms.NumberInput(attrs={
                                        'min': 2, 
                                        'max': 10,
                                        'class': 'form-control' })
        }
        help_texts = {
            'name': None,
            'channel': None,
        }
