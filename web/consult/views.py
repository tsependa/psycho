from collections import defaultdict
from datetime import timedelta, datetime

import uuid

from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from rest_framework.decorators import api_view

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from yandex_checkout import Configuration, Payment as YandexPayment

from consult.models import Theme, Specialist, Enroll, TimeSlot, Faq, Payment
from consult.utils.mail import pay_email_notify

Configuration.account_id = settings.KASSA_ACCOUNT
Configuration.secret_key = settings.KASSA_SECRET


@login_required
def user_office(request):
    user = User.objects.get(username=request.user.username)
    context = dict()
    context.pop("user", user)

    response = render(request, "office/office.html", context=context)
    # response.delete_cookie("specialist_id")
    # response.set_cookie("user_id", user.id)

    if hasattr(user, 'specialist'):
        response.set_cookie("specialist_id", user.specialist.id)

    return response


def consult(request):
    specialists = Specialist.objects.all()
    return render(request, "public/main.html",
                  context={'specialists': specialists})


def select(request):
    return render(request, "public/select.html",
                  context={})


def specialist(request, specialist_id):
    specialist = Specialist.objects.get(pk=specialist_id)
    theme_id = request.GET.get('theme', None)

    if theme_id != 'Undefined':
        recommends = Specialist.objects.all()[:6]
    else:
        recommends = Specialist.objects.all()[:6]
    return render(request, "public/specialist.html", context={'specialist': specialist, 'recommends': recommends})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            my_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, email=username, password=my_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def profile(request):
    return render(request, 'office/profile.html', {})


def faq(request):
    faqs = Faq.objects.all()
    return render(request, 'public/faq.html', {'faqs': faqs})


@login_required
def schedule(request):
    user = User.objects.get(username=request.user.username)
    specialist = user.specialist

    return render(request, 'office/schedule.html', {'specialist': specialist})


def user_enroll(request, timeslot_id):
    timeslot = TimeSlot.objects.get(pk=timeslot_id)
    specialist = timeslot.specialist
    return render(request, 'public/enroll.html', {'timeslot': timeslot, 'specialist': specialist})


def pay(request, timeslot_id):
    amount = 3400
    timeslot = TimeSlot.objects.get(pk=timeslot_id)
    user = create_user(request)
    enroll = Enroll.objects.create(timeslot_id=timeslot_id, user=user, )
    enroll.save()
    payment = Payment.objects.create(enroll=enroll, status="initial", amount=amount, )
    payment.save()
    yandex_payment = YandexPayment.create({
        "amount": {
            "value": amount,
            "currency": "RUB"
        },
        "payment_method_data": {
            "type": "bank_card"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": settings.KASSA_REDIRECT_URL
        },
        "capture": False,
        "description": "Консультация " + timeslot.specialist.middle_name + " " + timeslot.specialist.first_name
    }, uuid.uuid4())

    payment_id = yandex_payment.id
    payment.yandex_payment = payment_id
    payment.save()

    print(yandex_payment)
    return HttpResponseRedirect(yandex_payment.confirmation.confirmation_url)


def create_user(request):
    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        user = None

    if user is None:
        user = User.objects.create_user(email=request.POST['email'], username=request.POST['email'], password='123456')
        user.save()
        auth_user = authenticate(username=user.username, password='123456')
        login(request, auth_user)
    return user


def pay_approve(request):
    return render(request, 'public/enroll.html', {})


@login_required
def pay_success(request):
    return render(request, 'public/pay_success.html')


@api_view(['POST'])
def pay_notification(request):
    payment_id = request.data['object']['id']
    response = YandexPayment.capture(payment_id)
    print(response)
    payment = Payment.objects.get_or_create(yandex_payment=payment_id)
    payment.status = response.status
    payment.save()
    if not payment.notify:
        pay_email_notify(payment)
        payment.notify = True

    return Response(status=200)
