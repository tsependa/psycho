from django.contrib.auth.models import User
from django.db import models

# Create your models here.
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

    quote = models.TextField(blank=True)

    experience = models.IntegerField(blank=True)

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='female')

    degree = models.CharField(max_length=256, blank=True)

    education = models.TextField(blank=True)
    education_add = models.TextField(blank=True)

    themes = models.ManyToManyField(Theme, blank=True)
    methods = models.ManyToManyField(Method, blank=True)
    types = models.ManyToManyField(Type, blank=True)

    def __str__(self):
        return self.middle_name + " " + self.first_name + " " + self.last_name


class TimeSlot(models.Model):
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, related_name='timeslots')
    start_time = models.DateTimeField()
    duration = models.IntegerField(blank=True, default=60)

    @property
    def videoconf_url(self):
        return settings_prod.VIDEOCONF_URL + "/" + str(abs(hash(self.start_time)))


class Enroll(models.Model):
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='enrolls')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Payment(models.Model):
    STATUS_OPEN = "OPEN"
    STATUS_CANCELED = "CANCELED"
    STATUS_PENDING = "PENDING"
    STATUS_EXPIRED = "EXPIRED"
    STATUS_FAILED = "FAILED"
    STATUS_PAID = "PAID"

    STATUS_CHOICES = (
        (STATUS_OPEN, "open"),
        (STATUS_CANCELED, "canceled"),
        (STATUS_PENDING, "pending"),
        (STATUS_EXPIRED, "expired"),
        (STATUS_FAILED, "failed"),
        (STATUS_PAID, "paid")
    )

    enroll = models.ForeignKey(Enroll, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Faq(models.Model):
    question = models.TextField(blank=True)
    answer = models.TextField(blank=True)
    sequence = models.IntegerField()

    def __str__(self):
        return self.question
