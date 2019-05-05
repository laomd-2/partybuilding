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
import sys

from django.conf.urls import url
# from django.contrib import admin
from django.urls import path, include
from django.views import static
from django.views.generic import RedirectView
import xadmin
from user.views import RegisterView
from django.conf import urls
from . import views
from notice.tasks import *
from info.util import export_statistics


xadmin.autodiscover()


urlpatterns = [
    path('', xadmin.site.urls),
    path('notice/', include('notice.urls')),
    path('ueditor/', include('DjangoUeditor.urls')),
    url(r'^static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT}, name='static'),
    url(r'^media/(?P<path>.*)$', static.serve,
        {'document_root': settings.MEDIA_ROOT}, name='media'),
    path('favicon.ico', RedirectView.as_view(url='static/img/sy_dyw377.ico')),
    path('register/', RegisterView.as_view(), name='register'),
    path('info/member/export_statistics', export_statistics)
]
urls.handler403 = views.permission_denied

if settings.DEBUG:
    import debug_toolbar

    urlpatterns.append((path('__debug__/', include(debug_toolbar.urls))))

# if 'runserver' in sys.argv:
#     import threading
#     from robot.daka.producer import producer
#     from robot.daka.consumer import consume
#
#     threading.Thread(target=producer).start()
#     threading.Thread(target=consume).start()
