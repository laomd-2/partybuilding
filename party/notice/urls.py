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
from django.urls import path

from notice.tasks import *
from .views import *

urlpatterns = [
    path('firsttalk', get_first_talk),
    path('activist', get_activist),
    path('keydevelop', get_keydevelop),
    path('learningclass', get_learningclass),
    path('premember', get_premember),
    path('fullmember', get_fullmember),
    path('email/firsttalk', first_talk),
    path('email/activist', activist),
    path('email/keydevelop', key_develop_person),
    path('email/learningclass', learningclass),
    path('email/premember', pre_party_member1),
    path('email/fullmember', party_member)
]
