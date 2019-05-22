from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, HttpResponseRedirect
# Create your views here.
from django.views.decorators.cache import never_cache
from .forms import RegisterForm
from .models import User
from new_party.admin import site


class RegisterView(LoginView):
    template_name = 'register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '注册'
        context['site_title'] = site.site_title
        return context

    @never_cache
    def post(self, request, *args, **kwargs):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('username', None)
            if not user_name.isdigit():
                list(messages.get_messages(request))
                messages.error(request, '学号只能是数字。')
                return self.get(request)
            if User.objects.filter(username=user_name):
                list(messages.get_messages(request))
                messages.error(request, '账号已存在，请通过邮件找回密码。')
                return self.get(request)

            pass_word = request.POST.get('password', None)
            email = request.POST.get('email', None)
            # 实例化一个user_profile对象
            user_profile = User()
            user_profile.username = user_name

            member = user_profile.member
            # if member is None:
            #     list(messages.get_messages(request))
            #     messages.error(request, '您的动态信息未导入系统，因此不能注册。')
            #     return self.get(request)
            # user_profile._fullname = member['name']
            user_profile.email = email
            user_profile.is_active = user_profile.is_staff = True
            # 对保存到数据库的密码加密
            user_profile.password = make_password(pass_word)
            user_profile.save()
            # send_register_eamil(user_name, 'register')
            messages.success(request, '注册成功，请登录。')
            # return render(request, 'page_jump.html')
            return HttpResponseRedirect('/')
        return self.get(request)
