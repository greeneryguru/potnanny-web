from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse
from .models import Schedule
from .forms import ScheduleForm

def index(request):
    context = { 'title': 'Schedules' }

    try:
        context['payload'] = Schedule.objects.all()
    except:
        pass

    return render(request, 'schedule/index.html', context)


def create(request):
    form = None
    dow = [
        ('Sun', 64),
        ('Mon', 32),
        ('Tue', 16),
        ('Wed', 8),
        ('Thu', 4),
        ('Fri', 2),
        ('Sat', 1),
    ]
    if request.method == 'POST':
        print request.POST
        form = ScheduleForm(request.POST)
        if form.is_valid():
            sched = form.save()
            sched.save()
            return redirect('/schedule')
        else:
            return render(request, 'schedule/form.html', {'form': form, 'dow': dow})
    else:
        form = ScheduleForm()
        
    return render(request, 'schedule/form.html', {'form': form, 'dow': dow})


