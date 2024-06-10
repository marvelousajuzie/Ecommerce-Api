from django.shortcuts import render, get_object_or_404
from .serializer import *
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from datetime import datetime, timedelta
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .pagination import EcommercePagination
from django.core.mail import send_mail
from django.template.loader import render_to_string
from Ecommerce import settings
from .models import *
from .models import Category
from rest_framework.exceptions import PermissionDenied
from .serializer import CategorySerializer, ProductSerializer, CartSerializer,AddToCartSerializer, CartItemSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework  import request
            







def initial_payment(amount, email, redirect_url):
    url = "https://api.flutterwave.com/v3/payments"
    headers = {
        "Authorization": f"Bearer{settings.FLW_SEC_KEY}"
    }

    data = {
        "tx_ref": str(uuid.uuid4()),
        "amount": str(amount),
        "currency": "NGN",
        "redirect_url": redirect_url,
        "meta": {
            "consumers_id": 23,
            "consumers_mac": "92a3-912ba-1192a"
        },
        "customer": {
            "email": email,
            "phonenumber": "080*****81",
            "name": "Marvelous Ajuzie",
        },
        "customizations":
        {
            "title": "pied piper Payments",
            "logo": "http://www.piedpiper.com/app/theme/joystick-v27/images/logo-png",
        }
    }

    try:
        response = request.post(url, headers= headers, json= data)
        response_data = response.json()
        return Response(response_data)
    except requests.exceptions.RequestException as err:
        print("The payment didint go through")
        return Response({'error': str(err)}, status = 500)
    

        
                          #SECTION FOR PRODUCTVIEW   # (API= WORKING)

class ProductViewSet(viewsets.ModelViewSet):

    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def list(self, request, *args, **Kwargs):
        product = self.get_queryset()
        paginator = EcommercePagination()
        page = paginator.paginate_queryset(product, request)
        serializer = self.serializer_class(page, many= True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request, *args, **Kwargs):   # (API= WORKING)
        serializer = self.serializer_class(data= request.data)
        if serializer.is_valid(raise_exception= True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def patch(self, request, product_id):  #(API= WORKING)
        query_set = get_object_or_404(Product, product_id= product_id)
        serializer = self.serializer_class(query_set, data=request.data, partial= True)
        if serializer.is_valid(raise_exception= True):
            serializer.save()
            return Response({'message': 'Updated Successfully'}, status= status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, product_id, *args, **Kwargs):   #(API= WORKING)
        product = get_object_or_404( Product, product_id= product_id)
        product.delete()
        return Response({'message': 'Product Deleted Successfully'}, status= status.HTTP_200_OK)
    


                         # SECTION FOR CATEGORY  # (API= WORKING)
class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrive']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def list(self, request, *args, **Kwargs): # (API= WORKING)
        category = self.get_queryset()
        paginator = EcommercePagination
        page = paginator.paginate_queryset(category, request)
        serializer = self.serializer_class(page, many= True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request, *args, **Kwargs): #(API= WORKING)
        serializer = self.serializer_class(data= request.data)
        if serializer.is_valid(raise_exception= True):
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, category_id, *args, **Kwargs):  #(API= WORKING)
        query_set = get_object_or_404( Category, category_id = category_id)
        serializer = self.serializer_class(query_set, data= request.data)
        if serializer.is_valid(raise_exception= True):
            serializer.save()
            return Response(serializer.data, status= status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, category_id, *args, **Kwargs): #(API= WORKING)    
        query_set = get_object_or_404(Category, category_id= category_id)
        query_set.delete()
        return Response({'Deleted Sucessfully'}, status= status.HTTP_200_OK)



  # SECTTION FOR ADD TO CART

class CartView(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemView(viewsets.ModelViewSet):
    
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        cart_id = self.kwargs.get('cart_pk')
        if not cart_id:
            raise KeyError('cart_id not found in kwargs')
        return Cartitems.objects.filter(cart_id= cart_id)
        
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddToCartSerializer
        
        elif self.request.method == 'PATCH':
            return UpdateCartSerializer
        
        
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {"cart_id": self.kwargs['cart_pk']}

    

                 #SECTION FOR ORDER  # (API= WORKING)
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        return OrderSerializer
    

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_authenticated and isinstance(user, CustomUsers):
            serializer.save(user_id=user)
        else:
            raise PermissionDenied("Cannot create an order without a valid user.")


    def get_serializer_context(self):
        return {"user_id": self.request.user.id}
    

             #PAYMENT
    @action(detail= True, methods= ['POST'])
    def pay(self, request, pk):
        order = self.get_object()
        amount = order.total_price()
        email = request.user.email
        redirect_url = "http://127.0.0.1:9000/confirm/"
        return initial_payment(amount, email, redirect_url)



    
                     #AUTHENTICATION  SECTION        
# CUSTOMER REGISTRATION
class UsersRegisterViewSet(viewsets.ModelViewSet):
    serializer_class = UsersRegisterSerializer
    def get_queryset(self):
        return []

    def create(self, request, *args, **Kwargs):                                     #(API= WORKING)
        serializer = self.serializer_class(data= request.data)
        if serializer.is_valid(raise_exception= True):
            serializer.save()
            user = serializer.data
            return Response({'data': user}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


#CUSTOMER LOGIN
class UsersLoginViewSet(viewsets.ModelViewSet):
    serializer_class = UsersLoginSerializer

    @extend_schema(responses= serializer_class)

    def get_queryset(self):
        return []

    def create(self, request):                                 #(API= WORKING) 
        serializer = self.serializer_class(data= request.data)
        if serializer.is_valid():
            user= serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            RefreshTokens.objects.create(
            user= user,
            token = str(refresh))
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token), 
                'messages': 'Logged In Successfully',
            }, status= status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    










        #SECTION FOR CREATING ROLE
#IS ADMIN CREATE VIEW   
class AdminCreateViewSet(viewsets.ModelViewSet):
    queryset = CustomUsers.objects.all()
    serializer_class = AdminCreateSerializer

    def get_permissions(self):            #(API= WORKING)
        if self.action in ['create']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]






    
    
# ALL USERS FOR IS ADMIN
# class CustomUserView(viewsets.ModelViewSet):
#     serializer_class = CustomUserSerializer
#     queryset = CustomUsers.objects.get()

#     def get(self, request):
#         Users = self.get_queryset()
#         serializer = self.serializer_class(Users, many= True)
#         return Response(serializer.data, status= status.HTTP_200_OK)



















#CUSTOMER LOGOUT
class UserLogoutView(viewsets.ModelViewSet):

    def get_queryset(self):
        return []
    
    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken[refresh_token]
            token.blacklist()
            return Response(status= status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)      


 
# FOR CUSTOMER TO POST REVIEW
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer()
    queryset = Review.objects.all()

    def get_queryset(self):
        return []
    
    @action(detail= True, methods= ['post'])
    def review_product(self, request):
        # review = self.get_object()
        # product_id = request.data.get('product_id')
        # products = Product.objects.get(id = product_id)
        # review.comment(products)
        serializer = self.serializer(data= request.data)
        if serializer.is_valid():
            serializer.save(user= request.user)
            return Response(serializer.data, status= status.HTTP_200_OK)
        return Response(serializer.error, status= status.HTTP_400_BAD_REQUEST)

