from django.contrib import admin
from .models import group, topic, reply

# Register your models here.
admin.site.register([group])
admin.site.register([topic])
admin.site.register([reply])
