from django.db import models



class Cart(models.Model):
    cart_id = models.UUIDField(primary_key= True, default=uuid4, editable= False)
    user_id = models.ForeignKey(CustomUsers, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    price = models.IntegerField()
    quantity = models.IntegerField()
    sub_total = models.IntegerField() 
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.cart_id}"