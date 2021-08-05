from django.contrib import admin
from .models import Profile, Products,Order
# Register your models here.
admin.site.register(Profile)
admin.site.register(Products)
# admin.site.register(Details)
admin.site.register(Order)
