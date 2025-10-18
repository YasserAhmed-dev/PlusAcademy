from django.contrib import admin
from .models import Course, CustomUser,Lesson,Messages
# Register your models here.
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(CustomUser)
admin.site.register(Messages)
