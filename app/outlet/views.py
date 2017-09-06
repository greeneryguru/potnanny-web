import os
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse
from .models import Outlet
from .forms import OutletForm


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
    form = None

    if request.method == 'POST':
        form = OutletForm(request.POST, instance=o)
        if form.is_valid():
            outlet = form.save()
            outlet.save()
            return redirect('/outlet')

    else:
        form = OutletForm(instance=o)
        
    return render(request, 'outlet/form.html', {'form': form})


def delete(request, pk):
    if request.method != 'POST':
        raise Http404("Invalid request method")  

    o = get_object_or_404(Outlet, id=int(pk))
    o.delete()
    return redirect('/outlet')


def toggle(request, pk):
    if request.method != 'POST':
        raise Http404("Invalid request method")            

    cmd = '/var/www/greenery/bin/send'
    code = 12066304
    newstate = None
    try:
        o = get_object_or_404(Outlet, id=int(pk))
        code = code + (int(o.channel) << 1)
        if o.state == 1 or o.state is True:
            newstate = 0
        else:
            newstate = 1
            
        code = code + newstate
        o.state = newstate
        # issue command to 433mhz transmitter
        os.system("%s %d" % (cmd, code))
        o.save()
        return JsonResponse(o.simplified())
    except:
        return JsonResponse({})





