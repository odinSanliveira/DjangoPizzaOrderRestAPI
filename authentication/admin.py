from django.contrib import admin
from . models import User

# Register your models here.
@admin.register(User)
class UserAAdmin(admin.ModelAdmin):
    list_display=['id','username', 'email', 'is_active', 'is_verified']
    list_filter=['username', 'email', 'is_verified']
