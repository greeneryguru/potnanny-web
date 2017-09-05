from __future__ import unicode_literals
from django.shortcuts import render
from app.inventory.models import WirelessOutlet
# from app.measurement.models import OutletState

def outlets(request):
    context = {'title': 'Wireless Outlets'}
    try:
        outlets = WirelessOutlet.objects.all().order_by('name')
        context['payload'] = outlets
    except:
        pass

    return render(request, 'inventory/outlets.html', context)

def outlets(request, pk, state):
    context = {'title': 'Wireless Outlets'}
    try:
        outlets = WirelessOutlet.objects.all().order_by('name')
        context['payload'] = outlets
    except:
        pass

    return render(request, 'inventory/outlets.html', context)
