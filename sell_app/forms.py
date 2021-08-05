from .models import (
    Products,Profile, Order
)
from django import forms
from django.contrib.auth.models import User
  

class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Products
        fields = "__all__"
        exclude = ["user_name"]


class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ["phone"]


class OrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        exclude = ['seller','buyer_name','item','order_status']


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["username","email"]

