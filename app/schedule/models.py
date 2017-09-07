from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.core.validators import MaxValueValidator, MinValueValidator
from app.outlet.models import Outlet


# Create your models here.
@python_2_unicode_compatible
class Schedule(models.Model):
    outlet = models.ForeignKey(Outlet)
    on_time = models.TextField(
                        default="7:00 AM",
                        blank=False,
                        null=False,
                        help_text='Like "7:30 AM"')
    off_time = models.TextField(
                        default="7:00 PM",
                        blank=False,
                        null=False,
                        help_text='Like "12:00 PM"')
    days = models.IntegerField(
                        default=127,
                        blank=False,
                        null=False,
                        help_text='Days to run. Binary encoded')


    def __str__(self):
        d = ",".join(self.run_days())
        return "%s %s/%s (%s)" % (self.outlet, self.on_time,
                    self.off_time, d)


    def run_days(self):
        results = [];
        dow = [
            ('Su', 64),
            ('Mo', 32),
            ('Tu', 16),
            ('We', 8),
            ('Th', 4),
            ('Fr', 2),
            ('Sa', 1),
        ]
        if self.days == 127:
            results.append('Every Day')
        else:
            for item in dow:
                if (self.days & item[1]):
                    results.append(item[0])

        return results
    





