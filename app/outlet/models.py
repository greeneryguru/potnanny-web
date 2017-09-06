from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.core.validators import MaxValueValidator, MinValueValidator

@python_2_unicode_compatible
class Outlet(models.Model):
    name = models.CharField(
                        max_length=24, 
                        unique=True, 
                        blank=False, 
                        null=False,
                        help_text='Name of this outlet. Must be unique. 24 characters')
    channel = models.IntegerField(
                        default=1,
                        null=False,
                        blank=False,
                        unique=True,
                        validators=[MaxValueValidator(15), MinValueValidator(2)],
                        help_text='Channel number')
    state = models.BooleanField(
                        default=False, 
                        null=False, 
                        blank=False,
                        help_text='Device state. On(True) or Off(False)')

    def __str__(self):
        return self.name


    def simplified(self):
        return {'id': self.id, 'name': self.name, 'channel': self.channel,
                'state': self.state}
