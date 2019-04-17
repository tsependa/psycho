from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.

from consult.models import Theme, Specialist, Enroll, TimeSlot


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


def magic_payment(request):
    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        user = None

    if (user == None):
        user = User.objects.create_user(email=request.POST['email'], username=request.POST['email'], password='123456')
        user.save()
        auth_user = authenticate(username=user.username, password='123456')
        login(request, auth_user)
    enroll = Enroll.objects.create(timeslot_id=request.POST['timeslot_id'], user=user, )
    enroll.save()
    return redirect('office')


def profile(request):
    return render(request, 'office/profile.html', {})


@login_required
def schedule(request):
    response = render(request, 'office/schedule.html', {})
    user = User.objects.get(username=request.user.username)

    if hasattr(user, 'specialist'):
        response.set_cookie("specialist_id", user.specialist.id)

    return response
