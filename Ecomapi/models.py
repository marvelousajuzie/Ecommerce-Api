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
    role = models.ForeignKey(Role, on_delete= models.CASCADE, null= True)             
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

class RefreshTokens(models.Model):
    user = models.ForeignKey(CustomUsers, on_delete= models.CASCADE)
    token = models.CharField(max_length= 300, unique=True)
    created_at = models.DateTimeField(auto_now_add= True)
    expires_at = models.DateTimeField(auto_now_add= True)

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
    rating = models.CharField(max_length=50, default= 'N/A', blank= True, null=True)

def __str__(self):
    return self.name


class Cart(models.Model):
    cart_id = models.UUIDField(primary_key= True, default=uuid4, editable= False)
    creation_date = models.DateField(auto_now_add=True)
    
    class Meta:
        abstract = False


    def __str__(self):
        return f"{self.cart_id}"

class Cartitems(models.Model):
    cart = models.ForeignKey(Cart, related_name= 'Items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete= models.PROTECT)
    quantity = models.PositiveSmallIntegerField(default=1)
    



class Order(models.Model):
    order_id = models.UUIDField(primary_key= True, default= uuid4, editable=False)
    user_id = models.ForeignKey(CustomUsers, on_delete= models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add= True)
    shipping_address = models.CharField(max_length= 150)
    payment_method = models.CharField(max_length=100, default= 'Debit/Credit Cards')
    order_status= models.CharField(max_length=50, default= 'pending')   
     
    def __str__(self):
        return self.order_status
    
    @property
    def total_price(self):
        items = self.items.all()
        sub_total = sum(item.quantity * item.product.price for item in items)
        return sub_total


    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
   
    def __str__(self):
        return self.order

class Payment(models.Model):
    Payment_id = models.UUIDField(primary_key= True, default=uuid4, editable=False)
    user_id = models.ForeignKey(CustomUsers, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_amount = models.DecimalField(max_digits= 20, decimal_places=3)
    payment_date = models.DateField(auto_now_add= True)
    payment_status = models.CharField(max_length= 50, default= 'pending')
    payment_method = models.CharField(max_length=100, default= 'Debit/Credit Cards')
    
    
    def __self__(self):
        return self.payment_status


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
    


    




class Shipping(models.Model):
    shipping_id = models.UUIDField(primary_key= True, default=uuid4, editable=False)
    user_id = models.ForeignKey(CustomUsers, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length= 2000)
    shipping_method = models.CharField(max_length= 50)
    estimated_delivery_date = models.DateField(auto_created= True)


    def __str__(self):
        return self.shipping_id