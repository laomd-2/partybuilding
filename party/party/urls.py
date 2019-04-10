"""party URL Configuration

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
from django.conf.urls import url
# from django.contrib import admin
from django.urls import path
from django.views import static
from django.conf import settings
from django.views.generic import RedirectView
import xadmin
from user.views import RegisterView
import threading
import time
import sys
from django.conf import urls
from . import views
from robot.notice import *


xadmin.autodiscover()


urlpatterns = [
    path('', xadmin.site.urls),
    # path('ueditor/', include('DjangoUeditor.urls')),
    url(r'^static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT}, name='static'),
    url(r'^media/(?P<path>.*)$', static.serve,
        {'document_root': settings.MEDIA_ROOT}, name='media'),
    path('favicon.ico', RedirectView.as_view(url='static/img/sy_dyw377.ico')),
    path('register/', RegisterView.as_view(), name='register')
]
urls.handler403 = views.permission_denied


def start_listener():
    while 'runserver' in sys.argv:
        try:
            from robot import daka
        except Exception as e:
            print(e)
            time.sleep(5)

# threading.Thread(target=start_listener).start()

# write_application()
# first_talk()
