from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse
from .models import Schedule
from .forms import ScheduleForm

DOWS = [
    ('Su', 64),
    ('Mo', 32),
    ('Tu', 16),
    ('We', 8),
    ('Th', 4),
    ('Fr', 2),
    ('Sa', 1),
]

def index(request):
    context = { 'title': 'Schedules' }

    try:
        context['payload'] = Schedule.objects.all()
    except:
        pass

    return render(request, 'schedule/index.html', context)


def create(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)

        if form.is_valid():
            sched = form.save()
            sched.save()
            return redirect('/schedule')

    else:
        form = ScheduleForm()

    return render(request, 'schedule/form.html', 
                                    {'form': form, 'dow': DOWS})


def edit(request, pk):
    o = get_object_or_404(Schedule, id=int(pk))
    form = ScheduleForm(instance=o)

    if request.method == 'POST':
        form = ScheduleForm(request.POST, instance=o)
        if form.is_valid():
            sched = form.save()
            sched.save()
            return redirect('/schedule')
        
    return render(request, 'schedule/form.html', 
                    {'form': form, 'dow': DOWS, 'pk': pk})
        

def delete(request, pk):
    if request.method != 'POST':
        raise Http404("Invalid request method")  

    o = get_object_or_404(Schedule, id=int(pk))
    o.delete()
    return redirect('/schedule')


