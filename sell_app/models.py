from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = (
    ('F', 'Furniture'),
    ('Mob', 'Mobile and accessories'),
    ('Ele', 'Electronic and accessories'),
    ('com', 'Computer and accessories'),
    ('Tv', 'Tvs and appliances'),
)

class Profile(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100 )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=13)

    def __str__(self):
        return self.user.username


class Products(models.Model):
    product_name = models.CharField(max_length=20)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(choices = CATEGORY_CHOICES, max_length=4)
    description = models.TextField()
    location = models.CharField(max_length = 50)
    price = models.FloatField() 
    images1 = models.ImageField(upload_to = 'images/')
    
    def __str__(self) :
        return str(self.id)


class Order(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE,related_name = "seller" )
    buyer_name = models.ForeignKey(User, on_delete=models.CASCADE,related_name = "buyer" )
    my_price = models.FloatField()
    order_status = models.BooleanField(default=False)
    item = models.ForeignKey(Products, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id)

    