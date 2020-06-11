import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from twilio.rest import Client
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

load_dotenv()
FROM_NUMBERS = os.environ['FROM_NUMBERS'].split(',')
TO_NUMBERS = os.environ['TO_NUMBERS'].split(',')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'
Bootstrap(app)
twilio = Client()


class SendSMSForm(FlaskForm):
    from_phone = SelectField(
        'Sender\'s Phone Number',
        choices=[(number, number) for number in FROM_NUMBERS])
    to_phone = SelectField(
        'Recipient\'s Phone Number',
        choices=[(number, number) for number in TO_NUMBERS])
    message = StringField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')


def send_sms(from_phone, to_phone, message):
    twilio.messages.create(from_=from_phone, to=to_phone, body=message)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SendSMSForm()
    if form.validate_on_submit():
        try:
            send_sms(form.from_phone.data, form.to_phone.data,
                     form.message.data)
        except RuntimeError as ex:
            flash(str(ex))
        else:
            flash('SMS sent!')
            return redirect(url_for('index'))
    return render_template('index.html', form=form)
