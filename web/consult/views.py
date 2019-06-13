import secrets
import string
from collections import defaultdict
from datetime import timedelta, datetime

import uuid
from random import choice

from django.conf import settings
from django.db import models
from django.db.models import Count, Max, FilteredRelation, Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from yandex_checkout import Configuration, Payment as YandexPayment

from consult.forms import RegisterForm
from consult.models import Theme, Specialist, Enroll, TimeSlot, Faq, Payment, SupportQuestion, LandingRequest, Webinar, \
    WebinarEnroll
from consult.utils.mail import pay_user_email_notify, pay_specialist_email_notify, new_user_email_notify

Configuration.account_id = settings.KASSA_ACCOUNT
Configuration.secret_key = settings.KASSA_SECRET


@login_required
@ensure_csrf_cookie
def user_office(request):
    user = User.objects.get(username=request.user.username)
    enrolls = {}
    if hasattr(user, 'specialist'):
        enrolls = Enroll.objects.filter(timeslot__specialist_id=user.specialist.id)

    response = render(request, "office/office.html", {'user': user, 'enrolls': enrolls})

    if hasattr(user, 'specialist'):
        response.set_cookie("specialist_id", user.specialist.id)

    return response


def consult(request):
    specialists = Specialist.objects.all()
    return render(request, "public/main.html",
                  context={'specialists': specialists})


def select(request):
    specialists = Specialist.objects.all().filter(active=True)
    return render(request, "public/select.html",
                  context={'specialists': specialists})


def specialist(request, specialist_id):
    specialist = Specialist.objects.get(pk=specialist_id)
    theme_id = request.GET.get('theme', None)

    if theme_id != 'Undefined':
        recommends = Specialist.objects.all()[:6]
    else:
        recommends = Specialist.objects.all()[:6]
    return render(request, "public/specialist.html", context={'specialist': specialist, 'recommends': recommends})


@ensure_csrf_cookie
def signup(request):
    redirect_to = request.GET.get('next', None)
    if not redirect_to:
        redirect_to = request.POST.get('next', None)
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            my_password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=my_password)
            login(request, user)
            if not redirect_to:
                # redirect_to = settings.LOGIN_REDIRECT_URL
                return redirect('index')
            else:
                return redirect(redirect_to)
    else:
        form = RegisterForm()
    return render(request, 'registration/signup.html', {'form': form, 'next': redirect_to})


def profile(request):
    return render(request, 'office/profile.html', {})


def faq(request):
    faqs = Faq.objects.all()
    return render(request, 'public/faq.html', {'faqs': faqs})


@login_required
def schedule(request):
    user = User.objects.get(username=request.user.username)
    specialist = user.specialist

    response = render(request, 'office/schedule.html', {'specialist': specialist})

    if hasattr(user, 'specialist'):
        response.set_cookie("specialist_id", user.specialist.id)

    return response


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
        "description": "Консультация " + timeslot.specialist.middle_name + " " + timeslot.specialist.first_name,
        "receipt": {
            "items": [{
                "description": "Консультация " + timeslot.specialist.middle_name + " " + timeslot.specialist.first_name,
                "quantity": 1,
                "amount": {
                    "value": amount,
                    "currency": "RUB"
                },
                "vat_code": 1,
                "payment_subject": "service",
                "payment_mode": "full_prepayment"

            }],
            "tax_system_code": 3,
            "email": user.email,

        }
    }, uuid.uuid4())

    payment_id = yandex_payment.id
    payment.yandex_payment = payment_id
    payment.save()

    print(yandex_payment)
    return HttpResponseRedirect(yandex_payment.confirmation.confirmation_url)


def create_user(request):
    print(request.POST.get('email'))
    user = None
    if request.user.is_authenticated:
        try:
            user = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            user = None

    if user is None:
        try:
            user = User.objects.filter(email=request.POST.get('email')).first()
        except User.DoesNotExist:
            user = None

    if user is None:
        alphabet = string.ascii_letters + string.digits
        password = ''.join(choice(alphabet) for i in range(6))
        user = User.objects.create_user(email=request.POST.get('email'), username=request.POST.get('email'),
                                        password=password)
        user.save()
        new_user_email_notify(user, password)
        auth_user = authenticate(username=user.username, password=password)
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
    yandex_payment = YandexPayment.capture(payment_id)
    payment = Payment.objects.get(yandex_payment=payment_id)
    if payment:
        payment.status = yandex_payment.status
        payment.save()
        print(yandex_payment.id)
        print(yandex_payment.status)
        user = payment.enroll.user

        if not payment.notify:
            payment.notify = True
            payment.save()
            pay_user_email_notify(payment)
            pay_specialist_email_notify(payment)

    return Response(status=200)


def support(request):
    popup = False
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        question = request.POST.get("question")
        support_question = SupportQuestion.objects.create(name=name, email=email, phone=phone, question=question)
        support_question.save()
        popup = True
    return render(request, 'public/support.html', {'popup': popup})


def supervision(request):
    popup = False
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        question = request.POST.get("question")
        landing_request = LandingRequest.objects.create(name=name, email=email, phone=phone, question=question,
                                                        type="super")
        landing_request.save()
        popup = True
    return render(request, 'public/supervision.html', {'popup': popup})


@ensure_csrf_cookie
def webinars(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect('%s?next=%s' % (reverse('signup'), reverse('webinars')))
        else:
            webinar_id = request.POST.get("webinar_id")
            webinar_enroll = WebinarEnroll.objects.get_or_create(webinar_id=webinar_id, user_id=request.user.id)
    webinar_list = Webinar.objects.filter().annotate(
        user_enroll=Count('enrolls', Q(enrolls__user_id__exact=request.user.id)), )
    return render(request, 'public/webinars.html', {'webinars': webinar_list})


@ensure_csrf_cookie
def webinar(request, webinar_slug):
    webinar_item = Webinar.objects.get(slug=webinar_slug)
    webinar_enroll = WebinarEnroll.objects.filter(webinar=webinar_item, user_id=request.user.id) or None
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect('%s?next=%s' % (reverse('signup'), reverse('webinars')))
        else:
            webinar_enroll = WebinarEnroll.objects.get_or_create(webinar=webinar_item, user_id=request.user.id)
    return render(request, 'public/webinar.html', {'webinar': webinar_item, 'enroll': webinar_enroll})
