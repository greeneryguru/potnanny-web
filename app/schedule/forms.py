from django import forms
from .models import Schedule

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['outlet', 'on_time', 'off_time', 'days']
        widgets = {
            'on_time': forms.TextInput(attrs={
                                            'required': True,
                                            'class': 'form-control'}),
            'off_time': forms.TextInput(attrs={
                                            'required': True,
                                            'class': 'form-control'}),
            'days': forms.NumberInput(attrs={
                                            'required': True,
                                            'class': 'form-control'}),
        }
        help_texts = {
            # 'on_time': None,
            # 'off_time': None,
            'days': None,
        }
        
   
