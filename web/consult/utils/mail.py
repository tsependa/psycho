import os

import pytz
from datetime import timedelta
from django.conf import settings
from django.utils.timezone import make_aware
from sendgrid import Mail, SendGridAPIClient

from psycho import settings_prod

EXISTING_PAY_TEMPLATE_ID = 'd-d7dede3e1be14b6781e786ca9f71db5b'
NEW_USER_TEMPLATE_ID = 'd-b62f5d1e6ddc4457b3c5f2e4d9196f5e'
SPECIALIST_TEMPLATE_ID = 'd-51f583e5a81f41759fbab3fd432b0059'


def pay_user_email_notify(payment):
    start_time = payment.enroll.timeslot.start_time
    start_time = start_time + timedelta(hours=3)
    print(start_time)
    message = Mail(
        from_email='remind@xn--c1ajbknbbehlb3cxi.xn--p1ai',
        to_emails=payment.enroll.user.email,
        subject='new consult',
        html_content='<strong></strong>')
    message.dynamic_template_data = {
        "date": start_time.strftime('%d/%m/%G'),
        "time": start_time.strftime('%H:%M'),
        "link": payment.enroll.timeslot.videoconf_url,
        "specialist": payment.enroll.timeslot.specialist.full_name(),
        "email": payment.enroll.user.email,

    }

    message.template_id = EXISTING_PAY_TEMPLATE_ID
    message.template_id = NEW_USER_TEMPLATE_ID

    sendgrid_client = SendGridAPIClient(settings.SENDGRID_API_KEY)
    sendgrid_client.send(message)


def pay_specialist_email_notify(payment):
    start_time = payment.enroll.timeslot.start_time
    start_time = start_time + timedelta(hours=3)
    print(start_time)
    message = Mail(
        from_email='remind@xn--c1ajbknbbehlb3cxi.xn--p1ai',
        to_emails=payment.enroll.timeslot.specialist.user.email,
        subject='new consult',
        html_content='<strong></strong>')
    message.dynamic_template_data = {
        "date": start_time.strftime('%d/%m/%G'),
        "time": start_time.strftime('%H:%M'),
        "link": payment.enroll.timeslot.videoconf_url,
        "specialist": payment.enroll.timeslot.specialist.full_name(),
        "email": payment.enroll.user.email,

    }

    message.template_id = SPECIALIST_TEMPLATE_ID
    sendgrid_client = SendGridAPIClient(settings.SENDGRID_API_KEY)
    sendgrid_client.send(message)


def new_user_email_notify(user, password):
    print("sending password to ")
    print(user.email)
    message = Mail(
        from_email='remind@xn--c1ajbknbbehlb3cxi.xn--p1ai',
        to_emails=user.email,
        subject='new user',
        html_content='<strong></strong>')
    message.dynamic_template_data = {
        "email": user.email,
        "password": password
    }
    message.template_id = NEW_USER_TEMPLATE_ID
    sendgrid_client = SendGridAPIClient(settings.SENDGRID_API_KEY)
    sendgrid_client.send(message)
