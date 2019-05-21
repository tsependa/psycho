import os

from sendgrid import Mail, SendGridAPIClient

EXISTING_PAY_TEMPLATE_ID = "d-d7dede3e1be14b6781e786ca9f71db5b"
NEW_PAY_TEMPLATE_ID = ""
NEW_USER_TEMPLATE_ID = ""


def pay_email_notify(payment):
    message = Mail(
        from_email='remind@xn--c1ajbknbbehlb3cxi.xn--p1ai',
        to_emails=payment.enroll.user.email,
        subject='Новая консультация на Роспсихология.рф',
        html_content='')
    message.dynamic_template_data = {
        "date": payment.enroll.timeslot.start_time,
        "time": payment.enroll.timeslot.start_time,
        "link": payment.enroll.timeslot.videoconf_url,
        "specialist": payment.enroll.timeslot.specialist.middle_name
    }
    message.template_id = EXISTING_PAY_TEMPLATE_ID

    try:
        sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        sendgrid_client.send(message)
    except Exception as e:
        print(e)
