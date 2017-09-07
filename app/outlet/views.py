from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse
from .models import Outlet
from .forms import OutletForm
from app.schedule.models import Schedule
from lib.rfutils import TXChannelControl

def index(request):
    context = { 'title': 'Wireless Outlets' }

    try:
        context['payload'] = Outlet.objects.all()
    except:
        pass

    return render(request, 'outlet/index.html', context)


def create(request):
    form = None

    if request.method == 'POST':
        form = OutletForm(request.POST)
        if form.is_valid():
            outlet = form.save()
            outlet.save()
            return redirect('/outlet')
        else:
            return render(request, 'outlet/form.html', {'form': form})
    else:
        form = OutletForm()
        
    return render(request, 'outlet/form.html', {'form': form})


def edit(request, pk):
    o = get_object_or_404(Outlet, id=int(pk))
    scheds = Schedule.objects.filter(outlet=o)
    form = None
    
    if request.method == 'POST':
        form = OutletForm(request.POST, instance=o)
        if form.is_valid():
            outlet = form.save()
            outlet.save()
            return redirect('/outlet')

    else:
        form = OutletForm(instance=o)
        
    return render(request, 'outlet/form.html', 
                            {'form': form, 'pk': pk, 'schedules': scheds})


def delete(request, pk):
    if request.method != 'POST':
        raise Http404("Invalid request method")  

    o = get_object_or_404(Outlet, id=int(pk))
    o.delete()
    return redirect('/outlet')


def toggle(request, pk):
    if request.method != 'POST':
        raise Http404("Invalid request method")            

    o = get_object_or_404(Outlet, id=int(pk))
    tcc = TXChannelControl(send_command='/var/www/greenery/bin/send')

    if o.state == 1 or o.state is True:
        newstate = 0
    else:
        newstate = 1
        
    rval, msg = tcc.send_control(o.channel, newstate)
    if not rval:
        o.state = newstate
        o.save()

    return JsonResponse(o.simplified())





