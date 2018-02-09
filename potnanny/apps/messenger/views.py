from flask import render_template, redirect, request, session, \
    Blueprint, jsonify
from potnanny.extensions import db
from .models import TwilioAccount
from .forms import TwilioForm, TestMessageForm
import re

messenger = Blueprint('messenger', __name__,
                        template_folder='templates')


@messenger.route('/messenger/account', methods=['GET'])
def twilio_index():
    account = TwilioAccount.query.first()
    return render_template('messenger/index.html', 
        account=account,
        title="Messenger Settings")
    
    
@messenger.route('/messenger/account/<int:pk>/edit', methods=['GET','POST'])
@messenger.route('/messenger/account/create', methods=['GET','POST'])
def twilio_edit(pk=None):
    obj = None
    title = 'Add Twilio Account'

    if pk:
        title = 'Edit Twilio Account'
        obj = TwilioAccount.query.get_or_404(pk)

    form = TwilioForm(obj=obj)
    if request.method == 'POST' and form.validate_on_submit():
        if obj:
            form.populate_obj(obj)
        else:
            obj = TwilioAccount(form.sid.data, form.token.data, form.number.data)
            db.session.add(obj)

        db.session.commit()
        return redirect(request.args.get("next", "/messenger/account"))

    return render_template('messenger/form.html', 
        form=form,
        title=title,
        pk=pk)
    
@messenger.route('/messenger/account/<int:pk>/delete', methods=['POST'])
def twilio_delete(pk):
    o = TwilioAccount.query.get_or_404(pk)
    db.session.delete(o)
    db.session.commit()
    return redirect(request.args.get("next", "/messenger/account"))

@messenger.route('/messenger/message', methods=['GET','POST'])
def send_message():
    title = 'Send Test Message'

    form = TestMessageForm()
    if request.method == 'POST' and form.validate_on_submit():
        return redirect(request.args.get("next", "/messenger/account"))

    return render_template('messenger/message.html', 
        form=form,
        title=title)
    