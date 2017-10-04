from flask import render_template, redirect, request, session
from flask import jsonify
from flask_login import login_required
from app import app, db
from .models import MeasurementType, Measurement
import re
import datetime


@app.route('/', methods=['GET'])
@login_required
def dashboard_index():
    payload = []
    types = MeasurementType.query.all()
    now = datetime.datetime.now()
    past = now - datetime.timedelta(minutes=60)
    for t in types:
        dataset = [t.id, t.name, None, [], []]
        recent = Measurement.query.filter(Measurement.type_id == t.id, Measurement.date_time > past).order_by(Measurement.date_time.asc())

        dataset[2] = recent[-1].simplified()
        for d in recent:
            dataset[3].append(datetime.datetime.strftime(d.date_time, "%m/%d/%y %H:%M"))
            dataset[4].append(d.value)

        payload.append(dataset)

    return render_template('measurement/index.html', 
                title='Environment',
                payload=payload)


@app.route('/measurement_type/<pk>/latest', methods=['GET'])
def measurement_latest(pk):
    mt = MeasurementType.query.get_or_404(int(pk))
    latest = Measurement.query.filter(Measurement.type_id == mt.id).order_by(Measurement.date_time.desc()).first()
    return jsonify(latest.simplified())





