from __future__ import unicode_literals
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from app.inventory.models import Relay

# Create your models here.
@python_2_unicode_compatible
class Schedule(models.Model):
    name = models.CharField(
                        max_length=24, 
                        unique=True, 
                        blank=False, 
                        null=False,
                        default='My Schedule',
                        help_text='The name you refer to this schedule as. Must be unique. 24 characters')
    relay = models.ForeignKey(Relay)
    on_hour = models.IntegerField(
                        default=0,
                        blank=False,
                        null=False,
                        validators=[MaxValueValidator(0), 
                                    MinValueValidator(23)],
                        help_text='Hour to turn ON (0 to 23)'))
    on_min = models.IntegerField(
                        default=0,
                        blank=False,
                        null=False,
                        validators=[MaxValueValidator(0), 
                                    MinValueValidator(59)],
                        help_text='Minute to turn ON (0 to 59)'))
    off_hour = models.IntegerField(
                        default=0,
                        blank=False,
                        null=False,
                        validators=[MaxValueValidator(0), 
                                    MinValueValidator(23)],
                        help_text='Hour to turn OFF  (0 to 23)'))
    off_min = models.IntegerField(
                        default=0,
                        blank=False,
                        null=False,
                        validators=[MaxValueValidator(0), 
                                    MinValueValidator(59)],
                        help_text='Minute to turn OFF  (0 to 59)'))


