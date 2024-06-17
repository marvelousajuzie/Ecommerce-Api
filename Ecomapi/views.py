import uuid
import requests
from django.shortcuts import render, get_object_or_404
from .serializer import *
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from datetime import datetime, timedelta
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
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
from .view import *
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from .serializer import CategorySerializer, ProductSerializer, CartSerializer,AddToCartSerializer, CartItemSerializer
from rest_framework_simplejwt.tokens import RefreshToken

            




        
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
    
    def post(self, request, *args, **Kwargs):   
        serializer = self.serializer_class(data= request.data)
        if serializer.is_valid(raise_exception= True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def patch(self, request, product_id):  
        query_set = get_object_or_404(Product, product_id= product_id)
        serializer = self.serializer_class(query_set, data=request.data, partial= True)
        if serializer.is_valid(raise_exception= True):
            serializer.save()
            return Response({'message': 'Updated Successfully'}, status= status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, product_id, *args, **Kwargs):  
        product = get_object_or_404( Product, product_id= product_id)
        product.delete()
        return Response({'message': 'Product Deleted Successfully'}, status= status.HTTP_200_OK)
    


                         # SECTION FOR CATEGORY  # (API= WORKING)
class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = EcommercePagination

    def get_permissions(self):
        if self.action in ['list', 'retrive']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def list(self, request, *args, **Kwargs): 
        category = self.get_queryset()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(category, request)
        serializer = self.serializer_class(page, many= True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request, *args, **Kwargs): 
        serializer = self.serializer_class(data= request.data)
        if serializer.is_valid(raise_exception= True):
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, category_id, *args, **Kwargs): 
        query_set = get_object_or_404( Category, category_id = category_id)
        serializer = self.serializer_class(query_set, data= request.data)
        if serializer.is_valid(raise_exception= True):
            serializer.save()
            return Response(serializer.data, status= status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, category_id, *args, **Kwargs):    
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
            raise KeyError('cart_id not found')
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
    permission_classes = [IsAuthenticated]

    # def get_permissions(self):
    #     if self.action in ['list', 'retrieve']:
    #         permission_classes = [IsAdminUser]
    #     else:
    #         return Order.objects.filter(user=self.request.user)
    #     return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            Order.objects.all()
        else:
            return Order.objects.filter(user_id =self.request.user)


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
    def payment(self, request, pk):
        Order = self.get_object()
        try:
            amount = Order.total_price
            email = request.user.email
            order_id = str(uuid4())
            # redirect_url = "http://127.0.0.1:9000/api/Order/Confirm_pay/?id" + Order_id,
            return initial_payment(amount, email, order_id)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail= False, methods= ['POST'])
    def confirm_pay(self,request):
        order_id = request.GET.get("o_id")
        # try:
        #     uuid.UUID(order_id)
        # except ValueError:
        #     return Response({"error": f"'{order_id}' is not a valid UUID."},
        #                     status=status.HTTP_400_BAD_REQUEST)
        order = Order.objects.get(order_id=order_id)
        order.order_status = "confirmed"
        order.save()
        serializer = OrderSerializer(order)

        data = {
            "msg": "Payment was Sucessful",
            "data" : serializer.data
        }
        return Response(data)


    
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

    
#CUSTOMER LOGOUT
class LogoutViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def get_queryset(self):
        return []
    
    def create(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status= status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)      



class PasswordResetView(viewsets.ViewSet):
    def get_queryset(self):
        return []
    
    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        user = CustomUsers.objects.filter(email=email).first()
        if user:
            context = {
                'email': email,
                'domain': request.META['HTTP_HOST'],
                'site_name': 'YourSiteName',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'protocol': 'https' if request.is_secure() else 'http',
            }
            subject = 'Password Reset Request'
            message = render_to_string('password_reset_email.html', context)
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
            return Response({'message': 'Password reset instructions have been sent to your email.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'email does not exist.'}, status=status.HTTP_400_BAD_REQUEST)


# class PasswordResetConfirmView(viewsets.ModelViewSet):
#     def post(self, request, *args, **kwargs):
#         uidb64 = request.data.get('uidb64')
#         token = request.data.get('token')
#         password = request.data.get('password')

#         try:
#             uid = force_text(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#             user = None

#         if user and default_token_generator.check_token(user, token):
#             user.set_password(password)
#             user.save()
#             return Response({'message': 'Your password has been reset successfully.'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Invalid password reset link.'}, status=status.HTTP_400_BAD_REQUEST)









    
    
    #  ALL USERS FOR IS ADMIN
class AllUsersView(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]

    queryset = CustomUsers.objects.all()
    serializer_class = CustomUsersSerializer
    
    def get(self, request):
        Users = self.get_queryset()
        serializer = self.serializer_class(Users, many= True)
        return Response(serializer.data, status= status.HTTP_200_OK)



 
# FOR CUSTOMER TO POST REVIEW
class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('product_pk')
        if not product_id:
            raise KeyError('Product_id Not Found')
        return Review.objects.filter(product_id= product_id)
  

class ShippingViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch']

    permission_classes = [IsAuthenticated]

    serializer_class = ShippingSerializer
    queryset = Shipping.objects.all()


    def get_queryset(self):
        order_id = self.kwargs.get('order_pk')
        if not order_id:
            raise KeyError('order_id Not Found')
        return Shipping.objects.filter(order_id= order_id)

    def post(self, request):
        serializer = self.serializer_class(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializers.data, status= status.HTTP_200_OK)
        return Response(serializers.error)
    
    def update(self, request, shipping_id):
        query_set = get_object_or_404(Shipping, shipping_id= shipping_id)
        serializers = self.serializer_class(query_set,data=request.data, partial= True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,  status= status.HTTP_200_OK)
        return Response(serializers.errors)
        


        #SECTION FOR CREATING ROLE

class RoleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]

    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def get_queryset(self):
        return Role.objects.all()

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()



