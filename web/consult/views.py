from collections import defaultdict
from datetime import timedelta, datetime
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.

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
    print(timeslot)
    return render(request, 'public/enroll.html', {'timeslot': timeslot})
