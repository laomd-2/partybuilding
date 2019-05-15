# Generated by Django 2.1.7 on 2019-05-15 16:19

import django.contrib.auth.models
from django.db import migrations, models
import django.utils.timezone
import user.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='中山大学NetID，至多8位数字。', max_length=50, primary_key=True, serialize=False, validators=[user.validators.DigitUsernameValidator()], verbose_name='学号')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='邮箱')),
                ('is_staff', models.BooleanField(default=True, help_text='Designates whether the user can log into this admin site.', verbose_name='允许登录')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('_fullname', models.CharField(default='', editable=False, max_length=20, verbose_name='姓名')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '我的账号',
                'verbose_name_plural': '我的账号',
                'ordering': ('-last_login', 'username'),
                'abstract': False,
                'swappable': 'AUTH_USER_MODEL',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
