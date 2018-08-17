# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import User,Following_Blogger,Related_tb_name
# Register your models here.
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class BloggerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('name',               {'fields': ['following_name']}),
        ('头像', {'fields': ['avatar']}),
    ]
admin.site.register(User)
admin.site.register(Following_Blogger,BloggerAdmin)
admin.site.register(Related_tb_name)