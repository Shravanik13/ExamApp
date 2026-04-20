from django.contrib import admin

from examapp.models import Question, UserData

# Register your models here.
admin.site.register(Question)
admin.site.register(UserData)