from flask import render_template, redirect, request, session
from flask import jsonify
from flask_login import login_required
from sqlalchemy.sql import func
from app import app, db
from .models import MeasurementType, Measurement
from app.sensor.models import Sensor
import re
import datetime


@app.route('/', methods=['GET'])
@login_required
def dashboard_index():
    types = MeasurementType.query.all()
    
    return render_template('measurement/index.html', 
                title='Environment',
                payload=types)


@app.route('/measurement/type/<pk>/newest/avg', methods=['GET'])
def measurement_type_latest_avg(pk):
    mt = MeasurementType.query.get_or_404(int(pk))

    # build query in multiple parts
    newest = db.session.query(
        Measurement.date_time
    ).filter(
        Measurement.code == mt.code
    ).order_by(Measurement.date_time.desc()).first()[0]

    results = db.session.query(
        Measurement.code,
        func.avg(Measurement.value).label('average'),
        Measurement.date_time
    ).filter(
        Measurement.code == mt.code,
        Measurement.date_time == newest
    ).group_by(
        Measurement.date_time
    ).order_by(Measurement.date_time.desc()).first()

    if not results:
        return None

    return jsonify({
        'type-id': int(pk), 
        'type-name': mt.name, 
        'value': results[1],
        'date-time': datetime.datetime.strftime(newest, "%m/%d/%y %H:%M")
    })


@app.route('/measurement/type/<pk>/newest/avg/graph', methods=['GET'])
def measurement_type_latest_graph(pk, minutes=60):
    now = datetime.datetime.now()
    past = now - datetime.timedelta(minutes=minutes)
    dataset = {'labels': [], 'data': []}

    mt = MeasurementType.query.get_or_404(int(pk))
    
    results = db.session.query(
        Measurement.code,
        func.avg(Measurement.value).label('average'),
        Measurement.date_time
    ).filter(
        Measurement.code == mt.code,
        Measurement.date_time > past
    ).group_by(
        Measurement.date_time
    ).all()

    for row in results:
        dataset['labels'].append(datetime.datetime.strftime(row[2], "%m/%d/%y %H:%M"))
        dataset['data'].append(row[1])

    return jsonify(dataset)






