"""psycho URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views as views_flat
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve

from consult import views
from psycho import settings_prod
from psycho.routers import router

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('accounts/signup/', views.signup, name='signup'),
                  path('office/', views.user_office, name='office'),
                  path('office/profile', views.profile, name='profile'),
                  path('office/schedule', views.schedule, name='schedule'),
                  path('', views.consult, name='index'),
                  path('select', views.select, name='select'),
                  path('specialist/<int:specialist_id>', views.specialist, name='specialist'),
                  path('specialist/<int:specialist_id>/<int:theme_id>', views.specialist, name='specialist'),
                  path('enroll/<int:timeslot_id>', views.user_enroll, name='enroll'),
                  path('faq', views.faq, name='faq'),
                  path('pay/<int:timeslot_id>/', views.pay),
                  path('pay/success/<int:enroll_id>', views.pay_success),
                  path('api-auth/', include('rest_framework.urls')),
                  path('api/', include(router.urls)),
                  path('api/pay/notifications', views.pay_notification),
                  path('pages/', include('django.contrib.flatpages.urls')),

              ] + \
              static(settings_prod.STATIC_URL, document_root=settings_prod.STATIC_ROOT) + \
              static(settings_prod.MEDIA_URL, document_root=settings_prod.MEDIA_ROOT)
