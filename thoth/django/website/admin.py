from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(Question)
admin.site.register(Task)
admin.site.register(Api)
admin.site.register(TaskHistory)
