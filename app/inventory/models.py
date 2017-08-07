from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.core.validators import MaxValueValidator, MinValueValidator


@python_2_unicode_compatible
class Sensor(models.Model):
    CHOICES = (
        ('temp',        'Temperature'),
        ('temphumid',   'Temperature+Humidity'),
        ('moisture',    'Moisture'),
        ('light',       'Light'),
        # ('intrusion',   'Intrusion',),
    )  
    name = models.CharField(
                        max_length=24, 
                        unique=True, 
                        blank=False, 
                        null=False,
                        default='Sensor 1',
                        help_text='The name you refer to this sensor as. Must be unique. 24 characters')
    sensor_type = models.CharField(
                        max_length=12,
                        choices=CHOICES, 
                        default='temp')
    device = models.CharField(
                        max_length=24, 
                        unique=False, 
                        blank=True, 
                        null=True,
                        help_text='Device type/model info. 24 characters')
    gpio = models.IntegerField(
                        default=1,
                        null=False,
                        blank=False,
                        unique=True,
                        validators=[MaxValueValidator(31), MinValueValidator(0)],
                        help_text='GPIO pin number')
    active = models.BooleanField(
                        default=True, 
                        null=False, 
                        blank=False,
                        help_text='Device active or not. Inactive sensors will not be polled.')
    notes = models.TextField(null=True, blank=True,)

    def __str__(self):
        return self.name
        
                             
@python_2_unicode_compatible
class Relay(models.Model): 
    name = models.CharField(
                        max_length=24, 
                        unique=True, 
                        blank=False, 
                        null=False,
                        default='My Relay',
                        help_text='The name you will refer to this relay as. Must be unique. 24 characters')
    gpio = models.IntegerField(
                        default=1,
                        null=False,
                        blank=False,
                        unique=True,
                        validators=[MaxValueValidator(31), MinValueValidator(0)],
                        help_text='GPIO pin number')
    active = models.BooleanField(
                        default=True, 
                        null=False, 
                        blank=False,
                        help_text='Device active or not. Inactive relays will not be polled.')
    notes = models.TextField(
                        null=True, 
                        blank=True,)
                                             
    def __str__(self):
        return self.name
        

@python_2_unicode_compatible
class PollInterval(models.Model):
    CHOICES = (
        (2,     '2 minutes'),
        (5,     '5 minutes'),
        (10,    '10 minutes'),
        (15,    '15 minutes'),
        (30,    '30 minutes'),
    )  
    value = models.IntegerField(
                        choices=CHOICES, 
                        unique=True, 
                        blank=False, 
                        null=False,
                        default=5,
                        help_text='How frequently sensors will be polled.')

    def __str__(self):
        return "Every %d minutes" % self.value


@python_2_unicode_compatible
class Plugin(models.Model):
    name = models.CharField(
                        max_length=64, 
                        unique=True, 
                        blank=False, 
                        null=False)
    documentation = models.TextField(
                        blank=True, 
                        null=True)

    def __str__(self):
        return self.name

