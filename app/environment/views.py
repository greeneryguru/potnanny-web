
from __future__ import unicode_literals
from django.shortcuts import render
from app.inventory.models import Sensor
from app.measurement.models import SensorData

def index(request):
    context = {
        'title': 'Environmental',
        'payload': {},
    }

    feeders = SensorData.objects.values('sensor').distinct()
    for s in feeders:
        sensor = Sensor.objects.get(id=s['sensor'])
        for key in ('t','h'):
            newest = SensorData.objects.filter(sensor=sensor, data_type=key).latest('datetime')
            if sensor.name not in context['payload']:
                context['payload'][sensor.name] = []

            context['payload'][sensor.name].append(newest.value)

    return render(request, 'environment/index.html', context)


def humidity(request, sensor_id):
    context = {}
    try:
        s = Sensor.objects.get(id=sensor_id)
        newest = SensorData.objects.filter(sensor=s, data_type='h').latest('datetime')
        context = {'payload': newest}
    except:
        pass

    return render(request, 'environment/detail.html', context)


def temperature(request, sensor_id):
    context = {}
    try:
        s = Sensor.objects.get(id=sensor_id)
        newest = SensorData.objects.filter(sensor=s, data_type='t').latest('datetime')
        context = {'payload': newest}
    except:
        pass

    return render(request, 'environment/detail.html', context)


def light(request, sensor_id):
    context = {}
    try:
        s = Sensor.objects.get(id=sensor_id)
        newest = SensorData.objects.filter(sensor=s, data_type='l').latest('datetime')
        context = {'payload': newest}
    except:
        pass

    return render(request, 'environment/detail.html', context)

