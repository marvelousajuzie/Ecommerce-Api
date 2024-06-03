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
        fields = ['cart_id', 'cart', 'product', 'quantity', 'sub_total']

    def total(self, cartitem:Cartitems):
        return cartitem.quantity * cartitem.product.price



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


class OrderItemSerializer(serializers.ModelSerializer):
    product = SmallProductSerializer(many=False)

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=20, decimal_places=3, read_only=True)

    class Meta:
        model = Order
        fields = ['order_id', 'user_id', 'total_price', 'order_date', 'shipping_address', 'payment_method', 'order_status', 'items']

class CreateOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

class CreateOrderSerializer(serializers.ModelSerializer):
    cart_id = serializers.UUIDField()

    class Meta:
        model = Order
        fields = ['user_id', 'shipping_address', 'payment_method', 'cart_id']

    def create(self, validated_data):
        cart_id = validated_data.pop('cart_id')
        cart = Cart.objects.get(cart_id=cart_id)
        order = Order.objects.create(**validated_data)
        
        cart_items = Cartitems.objects.filter(cart=cart)
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity
            )
        return order

# IS ADMIN SERIALIZER
class AdminCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    password2 = serializers.CharField(write_only = True)

    role = serializers.SlugRelatedField(
        slug_field= 'name',
        queryset = Role.objects.all(),
        required = False,
        allow_null = True,
        error_messages = {'messages':'Role Does Not EXist'}
    )     
    class Meta:
        model = CustomUsers
        fields = ['email', 'username', 'password', 'password2', 'role']

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
            role = validated_data.get('role'),
            
        )
        return user

class RoleSerializer(serializers.ModelSerializer):
    class meta:
        model = Role
        fields = '__all__'

#USERS FOR IS ADMIN
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUsers
        fields = '__all__'


#REVIEW FOR IS ADMIN
# class ReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Review
#         fields = ['review_id', 'user_id', 'product_id', 'rating', 'comment', 'review_date']









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

class PasswordResetSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()





class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'





class CategorySerializer(serializers.ModelSerializer):
    class   Meta:
        model = Category
        fields = '__all__'

        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        field = '__all__'


 