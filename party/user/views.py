from crispy_forms.helper import FormHelper
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import LoginView as login
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, HttpResponseRedirect
# Create your views here.
from django.views.decorators.cache import never_cache
from xadmin.views.website import LoginView
from .forms import RegisterForm
from .models import User


class RegisterView(LoginView):
    login_template = None

    @never_cache
    def get(self, request, *args, **kwargs):
        context = self.get_context()
        helper = FormHelper()
        helper.form_tag = False
        helper.include_media = False
        context.update({
            'title': self.title,
            'helper': helper,
            'app_path': request.get_full_path(),
            REDIRECT_FIELD_NAME: request.get_full_path(),
        })
        defaults = {
            'extra_context': context,
            # 'current_app': self.admin_site.name,
            # 'authentication_form': self.login_form or AdminAuthenticationForm,
            'template_name': self.login_template or 'register.html',
        }
        self.update_params(defaults)
        # return login(request, **defaults)
        return login.as_view(**defaults)(request)

    @never_cache
    def post(self, request, *args, **kwargs):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('username', None)
            if not user_name.isdigit():
                # messages.error(request, '学号只能是数字。')
                return self.get(request)
            if User.objects.filter(username=user_name):
                messages.error(request, '账号已存在，请通过邮件找回密码。')
                return self.get(request)

            pass_word = request.POST.get('password', None)
            email = request.POST.get('email', None)
            # 实例化一个user_profile对象
            user_profile = User()
            user_profile.username = user_name
            user_profile.email = email
            user_profile.is_active = user_profile.is_staff = True
            # 对保存到数据库的密码加密
            user_profile.password = make_password(pass_word)
            user_profile.save()
            # send_register_eamil(user_name, 'register')
            messages.info(request, '注册成功。')
            # return render(request, 'page_jump.html')
            return HttpResponseRedirect('/')
        messages.error(request, '用户名或密码不合法。')
        return self.get(request)
