from typing import Any
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from .models import *





#PRODUCT SERIALIZER
class ProductSerializer(serializers.ModelSerializer):     
    class Meta:
        model = Product
        fields = ['product_id', 'name', 'description', 'price', 'stock_quantity', 'category', 'images', 'tags', 'rating']



class SmallProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_id', 'name', 'price']



                       #AUTHENTICATION SECTION
                       
# CUSTOMER REGISTER SERIALIZER
class UsersRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    password2 = serializers.CharField(write_only = True)

    class Meta:
        model = CustomUsers
        fields = ['email', 'username', 'password', 'password2']

    def validate_email(self, value):
        if CustomUsers.objects.filter(email= value).exists():
            raise serializers.ValidationError('Email Already In Use')
        return value
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Password Do Not Match')
        return data
    

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUsers.objects.create_user(
            email = validated_data['email'],
            username = validated_data['username'],
            password = validated_data.get('password'),
            
        )
        return user

 
              # LOGIN SERIALIZER
class UsersLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length =200)
    password = serializers.CharField(write_only = True)

    class Meta:
        model = CustomUsers
        fields = ['email', 'password']
            
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email= email, password= password)
            if not user:
                raise serializers.ValidationError('Invalid Credidentials')
        else:
            raise serializers.ValidationError('Must Include Email and Password')
        attrs['user'] = user
        return attrs
    
class LogoutSerializer(serializers.Serializer):
    pass





                #CART SECTION
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['cart_id']
 

class CartItemSerializer(serializers.ModelSerializer):
    product = SmallProductSerializer(many = False)
    sub_total = serializers.SerializerMethodField(method_name="total")
    class Meta:
        model = Cartitems
        fields = ['id', 'cart', 'product', 'quantity', 'sub_total']

    def total(self, cartitem:Cartitems):
        return cartitem.quantity * cartitem.product.price

class UpdateCartSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only = True)
    class Meta:
        model = Cartitems
        fields = ['id', 'quantity']


class AddToCartSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField()

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cartitem = Cartitems.objects.get(cart_id = cart_id, product_id= product_id)
            cartitem.quantity += quantity
            cartitem.save()
            self.instance = cartitem
        except:

            self.instance= Cartitems.objects.create(cart_id = cart_id,**self.validated_data )

        return self.instance
    
    class Meta:
        model = Cartitems
        fields = ['cart_id', 'product_id', 'quantity']



       # ORDER SECTION SERIALIZER
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

        # def get_price(self, orderitem):
        #     return self.product.price
        
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['order_id', 'cart', 'user_id', 'total_price','order_status', 'items']

    def get_total_price(self, order):
        return sum(item.quantity * item.product.price for item in order.items.all())

    
class CreateOrderSerializer(serializers.ModelSerializer):
    cart = serializers.UUIDField()

    class Meta:
        model = Order
        fields = [ 'cart', 'user_id']

    def create(self, validated_data):
        cart_id = validated_data.pop('cart')
        user_id = validated_data.pop('user_id')
        cart = Cart.objects.get(pk= cart_id)
        order = Order.objects.create(user_id=user_id, cart =cart, **validated_data)

        cart_items = Cartitems.objects.filter(cart_id=cart_id)
        order_items = []
        for cart_item in cart_items:
                order_item = OrderItem(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    )
                order_items.append(order_item)
        
        OrderItem.objects.bulk_create(order_items)
        return order
    


    # Shipping SECTION
class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = '__all__'





class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'permission']


    def create(self, validated_data):
        permissions_data = validated_data.pop('permissions', [])
        role = Role.objects.create(**validated_data)
        role.permissions = permissions_data
        role.save()
        return role
    

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.permissions = validated_data.get('permissions', instance.permissions)
        instance.save()
        return instance


#USERS FOR IS ADMIN
class CustomUserSerializer(serializers.ModelSerializer):
    class meta:
        model = CustomUsers
        fields = '__all__'


# REVIEW FOR IS ADMIN


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'


class PasswordResetSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()



class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields =['name', 'description']
        


class CustomUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUsers
        fields = ['email', 'username','is_staff']