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
    payload = None
    types = MeasurementType.query.all()
    now = datetime.datetime.now()
    past = now - datetime.timedelta(minutes=60)
    for t in types:
        # meas_type.id, meas_type.name, current temp, graph-labels, graph-data
        dataset = [t.id, t.name, None, [], []]
        results = db.session.query(
            Measurement.code,
            func.avg(Measurement.value).label('average'),
            Measurement.date_time
        ).filter(
            Measurement.code == t.code
        ).group_by(
            Measurement.date_time
        ).all()
        if not results:
            continue

        # set latest temp
        dataset[2] = {'value': results[-1][1], 'date_time': results[-1][2]}
        for row in results:
            dataset[3].append(datetime.datetime.strftime(row[2], "%m/%d/%y %H:%M"))
            dataset[4].append(row[1])

        if not payload:
            payload = []

        payload.append(dataset)

    return render_template('measurement/index.html', 
                title='Environment',
                payload=payload)


@app.route('/measurement_type/<pk>/latest', methods=['GET'])
def measurement_latest(pk):
    mt = MeasurementType.query.get_or_404(int(pk))
    latest = Measurement.query.filter(Measurement.type_id == mt.id).order_by(Measurement.date_time.desc()).first()
    if not latest:
        return None

    return jsonify(latest.simplified())





