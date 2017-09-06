from django import forms
from .models import Schedule

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['days', 'outlet', 'on_hour', 'on_min', 'off_hour', 'off_min']
        widgets = {
            'days': forms.HiddenInput(),
            'on_hour': forms.NumberInput(attrs={
                                            'required': True,
                                            'min': 0, 
                                            'max': 23,
                                            'class': 'form-control'}),
            'on_min': forms.NumberInput(attrs={
                                            'required': True,
                                            'min': 0, 
                                            'max': 59,
                                            'class': 'form-control'}),
            'off_hour': forms.NumberInput(attrs={
                                            'required': True,
                                            'min': 0, 
                                            'max': 23,
                                            'class': 'form-control'}),
            'off_min': forms.NumberInput(attrs={
                                            'required': True,
                                            'min': 0, 
                                            'max': 59,
                                            'class': 'form-control'}),
        }
        help_texts = {
            'on_hour': None,
            'on_min': None,
            'off_hour': None,
            'off_min': None,
        }
        
   
