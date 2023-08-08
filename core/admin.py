from django.contrib import admin
from core.models import Allcourse, Trainer, Register, Payments, Profile, ContactModelForm, Attendance

# Register your models here.
admin.site.register(Allcourse)
admin.site.register(Trainer)
admin.site.register(Register)
admin.site.register(Payments)
admin.site.register(ContactModelForm)
admin.site.register(Attendance)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'token', 'verify']
