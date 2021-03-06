from datetime import timedelta
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.datetime_safe import datetime

from psycho import settings_prod


class Theme(models.Model):
    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Published'),
        ('h', 'Hidden'),
    )

    title = models.CharField(max_length=512)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    sequence = models.IntegerField()

    def __str__(self):
        return self.title


class Method(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    sequence = models.IntegerField()

    def __str__(self):
        return self.title


class Type(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    sequence = models.IntegerField()

    def __str__(self):
        return self.title


class Specialist(models.Model):
    GENDER_CHOICES = (
        ('male', 'Мужской'),
        ('female', 'Женский'),
    )
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    middle_name = models.CharField(max_length=100, blank=True)

    avatar = models.ImageField(blank=True)
    avatar_mob = models.ImageField(blank=True)

    quote = models.TextField(blank=True)

    experience = models.IntegerField(blank=True)

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='female')

    degree = models.CharField(max_length=256, blank=True)

    education = models.TextField(blank=True)
    education_add = models.TextField(blank=True)

    themes = models.ManyToManyField(Theme, blank=True)
    methods = models.ManyToManyField(Method, blank=True)
    types = models.ManyToManyField(Type, blank=True)

    promo = models.IntegerField(blank=True, default=1)

    active = models.BooleanField(default=False)

    def __str__(self):
        return self.middle_name + " " + self.first_name + " " + self.last_name

    def next_slot(self):
        return self.timeslots.filter(start_time__gte=datetime.now() + timedelta(days=1)).exclude(
            enroll__isnull=False).order_by('start_time').first()

    def full_name(self):
        return self.middle_name + " " + self.first_name

    class Meta:
        ordering = ('promo',)


class TimeSlot(models.Model):
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, related_name='timeslots')
    start_time = models.DateTimeField()
    duration = models.IntegerField(blank=True, default=60)

    @property
    def videoconf_url(self):
        return settings_prod.VIDEOCONF_URL + "/" + str(abs(hash(self.start_time)))

    class Meta:
        ordering = ('start_time',)


class Enroll(models.Model):
    timeslot = models.OneToOneField(TimeSlot, on_delete=models.CASCADE, related_name='enroll')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


class WebinarAuthor(models.Model):
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    middle_name = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.middle_name + " " + self.first_name + " " + self.last_name


class Webinar(models.Model):
    STATUS_CHOICES = (
        ('hidden', 'Скрыт'),
        ('enroll_open', 'Запись открыта'),
        ('enroll_closed', 'Запись закрыта'),
        ('ended', 'Завершен')
    )

    name = models.CharField(max_length=255, blank=True)
    slug = models.CharField(max_length=50, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    start_date = models.DateTimeField()
    duration = models.IntegerField(default=60)
    themes = models.TextField(null=True, blank=True)
    authors = models.ManyToManyField(WebinarAuthor, blank=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='hidden')
    image = models.ImageField(blank=True)
    video_url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class WebinarEnroll(models.Model):
    webinar = models.ForeignKey(Webinar, on_delete=models.CASCADE, related_name='enrolls', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


class Payment(models.Model):
    TYPE_CHOICES = (
        ('consult', 'Консультация'),
        ('webinar', 'Вебинар'),
    )
    enroll = models.OneToOneField(Enroll, on_delete=models.CASCADE, related_name='payment', blank=True, null=True)
    webinar_enroll = models.OneToOneField(WebinarEnroll, on_delete=models.CASCADE, related_name='payment', blank=True,
                                          null=True)
    status = models.CharField(max_length=50)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='consult')
    notify = models.BooleanField(default=False)
    yandex_payment = models.CharField(max_length=50, blank=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    payload = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Faq(models.Model):
    question = models.TextField(blank=True)
    answer = models.TextField(blank=True)
    sequence = models.IntegerField()

    def __str__(self):
        return self.question


class SupportQuestion(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    phone = models.TextField(blank=True, null=True)
    question = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class LandingRequest(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    phone = models.TextField(blank=True, null=True)
    question = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
