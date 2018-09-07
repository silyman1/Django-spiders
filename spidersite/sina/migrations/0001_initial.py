# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_register_time', models.DateTimeField(auto_now_add=True, verbose_name=b'date to register')),
                ('nickname', models.CharField(default=b'\xe7\x94\xa8\xe6\x88\xb7', max_length=200)),
                ('last_seen', models.DateTimeField(auto_now_add=True)),
                ('avatar', models.CharField(default=b'avatar-default.jpg', max_length=200)),
                ('sina_username', models.CharField(max_length=200)),
                ('sina_password', models.CharField(max_length=200)),
                ('brief', models.CharField(default=b'\xe6\x9a\x82\xe6\x97\xa0', max_length=200)),
                ('barcode', models.CharField(default=b'weixin.jpg', max_length=200)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                (b'objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Following_Blogger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('following_name', models.CharField(max_length=200)),
                ('avatar', models.CharField(default=b'avatar-default.jpg', max_length=200)),
                ('last_vist', models.DateTimeField(auto_now_add=True)),
                ('brief', models.CharField(default=b'\xe6\x9a\x82\xe6\x97\xa0', max_length=200)),
                ('click_count', models.IntegerField(default=0, null=True)),
                ('following_num', models.IntegerField(default=0, null=True)),
                ('follower_num', models.IntegerField(default=0, null=True)),
                ('owner', models.ManyToManyField(related_name='owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
