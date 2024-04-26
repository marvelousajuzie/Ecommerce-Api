from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from uuid import uuid4



class Role(models.Model):
    name = models.CharField(max_length= 300)
    permission = models.JSONField(default= list)

    def __str__(self):
        return self.name


class CustomUsers(AbstractUser):                                     
    email= models.EmailField(unique= True, verbose_name= _('Email Address'))
    username = models.CharField(max_length=200, verbose_name= _('Username'))
   
    is_staff = models.BooleanField('is_staff', False)
    role = models.ForeignKey(Role, on_delete= models.SET_NULL, null=True, blank=True)             

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return self.email
    

class User(models.Model):
    user = models.OneToOneField(CustomUsers, on_delete= models.PROTECT, primary_key= True)
    address = models.CharField(max_length= 200, verbose_name= _('Address'))
    phone_num = models.IntegerField()
    paymethod = {
        'credit': "Credit",
        'card': 'Card',
        'paypal': 'Paypal',
    }
    payment_method = models.CharField(max_length=200, choices= paymethod)

class RefreshToken(models.Model):
    user = models.ForeignKey(CustomUsers, on_delete= models.CASCADE)
    token = models.CharField(max_length= 300, unique=True)
    created_at = models.DateTimeField(auto_now_add= True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return self.expires_at > timezone.now()






class Product(models.Model): 
    product_id = models.UUIDField(primary_key= True, default= uuid4, editable= False)
    name = models.CharField(max_length= 250)
    description = models.TextField()
    price = models.DecimalField(max_digits= 20, decimal_places=3)
    stock_quantity= models.IntegerField()
    category = models.CharField(max_length= 300, blank= True)
    images = models.ImageField(upload_to='images/')
    tags = models.CharField(max_length=250, blank=True)
    rating = models.CharField(max_length=50, default= 'N/A')

def __str__(self):
    return self.name


class Order(models.Model):
    order_id = models.UUIDField(primary_key= True, default= uuid4, editable=False)
    user_id = models.ForeignKey(CustomUsers, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    total_price = models.IntegerField()
    order_date = models.DateField(auto_now_add= True)
    order_status= models.CharField(max_length=50, default= 'pending')
    shipping_address = models.CharField(max_length= 150)
    paymethod = {
        'credit': "Credit",
        'card': 'Card',
        'paypal': 'Paypal',
    }

    payment_method = models.CharField(max_length=100, choices= paymethod)

    def __str__(self):
        return f"{self.order_id}  {self.user_id.username}"
    


class Payment(models.Model):
    Payment_id = models.UUIDField(primary_key= True, default=uuid4, editable=False)
    user_id = models.ForeignKey(CustomUsers, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_amount = models.IntegerField()
    payment_date = models.DateField(auto_now_add= True)
    payment_status = models.CharField(max_length= 50, default= 'pending')
    paymethod = {
        'credit': "Credit",
        'card': 'Card',
        'paypal': 'Paypal',
    }
    payment_method = models.CharField(max_length=200, choices= paymethod)
    
    
    def __self__(self):
        return self.Payment_id


class Category(models.Model):
    category_id = models.UUIDField(primary_key= True, default=uuid4, editable=False)
    name = models.CharField(max_length= 300)
    description = models.TextField()

    def __str__(self):
        return self.name
    

class Review(models.Model):
    review_id = models.UUIDField(primary_key= True, default=uuid4, editable=False)
    user_id = models.ForeignKey(CustomUsers, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete= models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    review_date = models.DateTimeField(auto_now_add= True)


    def __str__(self):
        return f"{self.review_id}"
    

class Cart(models.Model):
    cart_id = models.UUIDField(primary_key= True, default=uuid4, editable= False)
    user_id = models.ForeignKey(CustomUsers, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    total_price = models.IntegerField()
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.cart_id}"


class Shipping(models.Model):
    shipping_id = models.UUIDField(primary_key= True, default=uuid4, editable=False)
    user_id = models.ForeignKey(CustomUsers, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length= 2000)
    shipping_method = models.CharField()
    estimated_delivery_date = models.DateField(auto_created= True)


    def __str__(self):
        return self.shipping_id