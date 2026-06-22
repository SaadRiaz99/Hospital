from django.contrib import admin
# import models
from app.models import signup, Appointment , Login
# Service model removed; admin registration deleted.

admin.site.register(signup)
admin.site.register(Appointment)
admin.site.register(Login)

