from django.contrib.auth.hashers import make_password
from django.shortcuts import render
# Create your views here.
from django.views.decorators.cache import never_cache
from xadmin.views.website import LoginView
from .forms import RegisterForm
from .models import User


class RegisterView(LoginView):
    login_template = 'register.html'

    @never_cache
    def post(self, request, *args, **kwargs):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('username', None)
            if User.objects.filter(username=user_name):
                return self.get(request)

            pass_word = request.POST.get('password', None)
            # 实例化一个user_profile对象
            user_profile = User()
            user_profile.username = user_name
            user_profile.is_active = user_profile.is_staff = True
            # 对保存到数据库的密码加密
            user_profile.password = make_password(pass_word)
            user_profile.save()
            # send_register_eamil(user_name, 'register')
            return render(request, 'page_jump.html')
        return self.get(request)
