from django.contrib import admin

# Register your models here.
from django.contrib import admin
from core.models import *
# Register your models here.
admin.site.register(blog_model)

admin.site.register(User)
admin.site.register(ourTeam)