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


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'



class CartSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(many= False)
    cart_id = serializers.UUIDField(read_only = True)
    class Meta:
        model = Cart
        fields = ['cart_id']



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
            #    return {'user': user}

class PasswordResetSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_id', 'user_id', 'products', 'total_price', 'order_date', 'order_status', 'shipping_address', 'payment_method']
        read_only_fields = ['total_price']



class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_id', 'user_id', 'products', 'total_price', 'order_date', 'order_status', 'shipping_address', 'payment_method']
        read_only_fields = ['total_price']
        
    def create(self, validated_data):
        products_data = validated_data.pop('products')
        total_price = sum(product.price for product in products_data)
        order = Order.objects.create(**validated_data, total_price=total_price)
        order.products.set(products_data)
        return order
    


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'




        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        field = '__all__'


 