import os

import pytz
from datetime import timedelta
from django.conf import settings
from django.utils.timezone import make_aware
from sendgrid import Mail, SendGridAPIClient

from psycho import settings_prod

EXISTING_PAY_TEMPLATE_ID = 'd-51f583e5a81f41759fbab3fd432b0059'
NEW_PAY_TEMPLATE_ID = 'd-b62f5d1e6ddc4457b3c5f2e4d9196f5e'
NEW_USER_TEMPLATE_ID = ""


def pay_email_notify(payment, password=None):
    user_timezone = pytz.timezone(settings.TIME_ZONE)
    start_time = payment.enroll.timeslot.start_time
    start_time = start_time + timedelta(hours=3)
    print(start_time)
    message = Mail(
        from_email='remind@xn--c1ajbknbbehlb3cxi.xn--p1ai',
        to_emails=payment.enroll.user.email,
        subject='new consult',
        html_content='<strong>and easy to do anywhere, even with Python</strong>')
    message.dynamic_template_data = {
        "date": start_time.strftime('%d %b'),
        "time": start_time.strftime('%H:%M'),
        "link": payment.enroll.timeslot.videoconf_url,
        "specialist": '',
        "email": payment.enroll.user.email,
        "password": password,
    }
    if password is None:
        message.template_id = EXISTING_PAY_TEMPLATE_ID
    else:

        message.template_id = NEW_PAY_TEMPLATE_ID

    sendgrid_client = SendGridAPIClient(settings.SENDGRID_API_KEY)
    sendgrid_client.send(message)

