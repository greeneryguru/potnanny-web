from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.core.validators import MaxValueValidator, MinValueValidator
from app.outlet.models import Outlet


# Create your models here.
@python_2_unicode_compatible
class Schedule(models.Model):
    outlet = models.ForeignKey(Outlet)
    on_hour = models.IntegerField(
                        default=0,
                        blank=False,
                        null=False,
                        validators=[MaxValueValidator(23), 
                                    MinValueValidator(0)],
                        help_text='Hour to turn ON (0 to 23)')
    on_min = models.IntegerField(
                        default=0,
                        blank=False,
                        null=False,
                        validators=[MaxValueValidator(59), 
                                    MinValueValidator(0)],
                        help_text='Minute to turn ON (0 to 59)')
    off_hour = models.IntegerField(
                        default=0,
                        blank=False,
                        null=False,
                        validators=[MaxValueValidator(23), 
                                    MinValueValidator(0)],
                        help_text='Hour to turn OFF  (0 to 23)')
    off_min = models.IntegerField(
                        default=0,
                        blank=False,
                        null=False,
                        validators=[MaxValueValidator(59), 
                                    MinValueValidator(0)],
                        help_text='Minute to turn OFF  (0 to 59)')
    days = models.IntegerField(
                        default=0,
                        blank=False,
                        null=False,
                        help_text='Days to run. Binary encoded')


    def __str__(self):
        return "%s ON=%02d:%02d OFF=%02d:%02d" % (self.outlet, self.on_hour,
                    self.on_min, self.off_hour, self.off_min)


