from collections import defaultdict
from datetime import timedelta, datetime

import uuid

from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from yandex_checkout import Configuration, Payment

from consult.models import Theme, Specialist, Enroll, TimeSlot, Faq


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
    next_slot = specialist.timeslots.filter(start_time__gte=datetime.now()).order_by('start_time').first()
    return render(request, "public/specialist.html", context={'specialist': specialist, 'next_slot': next_slot})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            my_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=my_password)
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


Configuration.account_id = 602385
Configuration.secret_key = "test_iHkZR98UHAIn2h-UzFhLtiSFaXCY14YZLC7w85BvOKw"


def pay(request, timeslot_id):
    timeslot=TimeSlot.objects.get(pk=timeslot_id)
    payment = Payment.create({
        "amount": {
            "value": "3400.00",
            "currency": "RUB"
        },
        "payment_method_data": {
            "type": "bank_card"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "http://localhost:9000/office"
        },
        "capture": True,
        "description": "Консультация 1 "+timeslot.specialist.middle_name+" "+timeslot.specialist.first_name
    }, uuid.uuid4())

    return HttpResponseRedirect(payment.confirmation.confirmation_url)


class YandexNotification(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        payment_id = request.data['object']['id']
        Payment.capture(payment_id)

        return Response(status=200)
