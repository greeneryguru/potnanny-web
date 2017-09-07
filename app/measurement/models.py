from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import django.utils.timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from app.inventory.models import Sensor, Relay

@python_2_unicode_compatible
class SensorData(models.Model):
    CHOICES = (
        ('t',    'Temperature'),
        ('h',    'Humidity'),
        ('m',    'Moisture'),
        ('l',    'Light'),
    )    
    sensor = models.ForeignKey(Sensor)
    data_type = models.CharField(max_length=2,
                        choices=CHOICES, 
                        null=True, 
                        blank=True)
    value = models.DecimalField(null=True, 
                        blank=True,
                        max_digits=8, decimal_places=2)
    datetime = models.DateTimeField(default=django.utils.timezone.now,
                        blank=True,
                        null=True)  
                           
    def __str__(self):
        return ",".join((str(self.sensor), 
                        self.data_type,
                        "%0.2f" % self.value, 
                        str(self.datetime)))


@python_2_unicode_compatible
class RetentionPeriod(models.Model):
    CHOICES = (
        (30,    '30 days'),
        (60,    '60 days'),
        (90,    '90 days'),
        (180,   '180 days'),
        (365,   '1 year'),
    )  
    value = models.IntegerField(choices=CHOICES,
                        unique=True, 
                        blank=False, 
                        null=False,
                        default=60,
                        validators=[MaxValueValidator(365), MinValueValidator(1)],
                        help_text='How long to store sensor data for')

    def __str__(self):
        return "%d days" % self.value


@python_2_unicode_compatible
class TempDisplay(models.Model):
    CHOICES = (
        (0,    'Celsius'),
        (1,    'Fahrenheit'),
    )  
    value = models.IntegerField(choices=CHOICES,
                        unique=True, 
                        blank=False, 
                        null=False,
                        default=0,
                        validators=[MaxValueValidator(1), MinValueValidator(0)],
                        help_text='Temperature display')

    def __str__(self):
        if self.value == 0:
            return 'Celsius'
        else:
            return 'Fahrenheit'


