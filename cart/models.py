from django.db import models
from django.contrib.auth.models import User
from item.models import Item
# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User,related_name= 'customers',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    
class cartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    item= models.ForeignKey(Item, related_name = 'cartItems',on_delete=models.CASCADE)
    created_at = models.DateTimeField (auto_now=True)
    quantity = models.PositiveIntegerField(default=1)


class order(models.Model):
    user = models.ForeignKey(User,related_name= 'buyers',on_delete=models.CASCADE)
    items = models.ManyToManyField(cartItem,related_name='orders')
    created_at = models.DateTimeField(auto_now=True)
    total_price = models.FloatField()


