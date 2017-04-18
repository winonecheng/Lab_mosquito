from django.contrib import admin
from .models import User, Dengue, Flu
# Register your models here.

admin.site.register(User)
admin.site.register(Dengue)
admin.site.register(Flu)
