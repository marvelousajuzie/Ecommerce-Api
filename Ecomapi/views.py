import uuid
from django.shortcuts import render, get_object_or_404
from .serializer import *
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from datetime import datetime, timedelta
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from .filltering import ProductFilter
from rest_framework.response import Response
from django.db import transaction
from .pagination import EcommercePagination
from django.core.mail import send_mail
from django.template.loader import render_to_string
from Ecommerce import settings
from .models import *
from .permission import CAN_MANAGE_PRODUCTS, CAN_MANAGE_ORDERS, CAN_MANAGE_CATEGORIES
from .models import Category
import logging
from .view import *
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from .serializer import CategorySerializer, ProductSerializer, CartSerializer,AddToCartSerializer, CartItemSerializer
from rest_framework_simplejwt.tokens import RefreshToken

            




        
                          #PRODUCT VIEWSET           (API = WORKING)
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by('name')
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def list(self, request):
        product = self.get_queryset()
        paginator = EcommercePagination()
        page = paginator.paginate_queryset(product, request)
        serializer = self.serializer_class(page, many= True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request):   
        serializer = self.serializer_class(data= request.data)
        if serializer.is_valid(raise_exception= True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def put(self, request, product_id):  
        query_set = get_object_or_404(Product, product_id= product_id)
        serializer = self.serializer_class(query_set, data=request.data,  partial= True)
        if serializer.is_valid(raise_exception= True):
            serializer.save()
            return Response({'message': 'Updated Successfully'}, status= status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, product_id):  
        product = get_object_or_404( Product, product_id= product_id)
        product.delete()
        return Response({'message': 'Product Deleted Successfully'}, status= status.HTTP_200_OK)
    


                        #CATEGORY VIEWSET     (API = WORKING)
class CategoryViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = EcommercePagination

    def get_permissions(self):
        if self.action in ['list', 'retrive']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def list(self, request): 
        category = self.get_queryset()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(category, request)
        serializer = self.serializer_class(page, many= True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request): 
        serializer = self.serializer_class(data= request.data)
        if serializer.is_valid(raise_exception= True):
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, category_id): 
        query_set = get_object_or_404( Category, category_id = category_id)
        serializer = self.serializer_class(query_set, data= request.data)
        if serializer.is_valid(raise_exception= True):
            serializer.save()
            return Response(serializer.data, status= status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, category_id):    
        query_set = get_object_or_404(Category, category_id= category_id)
        query_set.delete()
        return Response({'Deleted Sucessfully'}, status= status.HTTP_200_OK)



 
                      #CART VIEWSET       (API = WORKING)
class CartView(mixins.CreateModelMixin,mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    


class CartItemView(mixins.CreateModelMixin,mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Cart.objects.none()
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Cartitems.objects.none()
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

    

                 #ORDER VIEWSET                (API = WORKING)
class OrderViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post','delete']
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Order.objects.all()
        return Order.objects.filter(user_id =self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        return OrderSerializer
    

    def create(self, request):
        user = self.request.user
        if user.is_authenticated and isinstance(user, CustomUsers):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user_id=user)
            return Response({'message': 'Ordered Sucessfully'}, status= status.HTTP_201_CREATED)
        else:
            raise PermissionDenied("Cannot create an order without a valid user.")
    

                #PAYMENT VIEWSET                (API = WORKING)
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
#USER REGISTER VIEWSET                                (API = WORKING)
class UsersRegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UsersRegisterSerializer

    def create(self, request, *args, **Kwargs):                                     #(API= WORKING)
        serializer = self.serializer_class(data= request.data)
        if serializer.is_valid(raise_exception= True):
            serializer.save()
            user = serializer.data
            return Response({'data': user}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


                    #USER LOGIN VIEWSET           (API = WORKING)
class UsersLoginViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UsersLoginSerializer
    
    def create(self, request):                                 
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

    
#CUSTOMER LOGOUT                               (API = WORKING)
class LogoutViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def create(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status= status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)      

    
                        #ALLUSERS VIEWSET   (API = WORKING)
class AllUsersView(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAdminUser]

    queryset = CustomUsers.objects.all()
    serializer_class = CustomUsersSerializer
    
    def get(self, request):
        Users = self.get_queryset()
        serializer = self.serializer_class(Users, many= True)
        return Response(serializer.data, status= status.HTTP_200_OK)



                             #REVIEW VIEWSET            (API = WORKING)
class ReviewViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('product_pk')
        if not product_id:
            raise KeyError('Product_id Not Found')
        return Review.objects.filter(product_id= product_id)
  
 

                              #SHIPPING VIEWSET                  (API = WORKING)
class ShippingViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch']

    permission_classes = [IsAuthenticated]
    queryset = Shipping.objects.none()
   
    serializer_class = ShippingSerializer

    def get_queryset(self):
        if getattr(self, 'Swagger_Fake_view', False):
            return Shipping.objects.all()
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
        

                             #ROLE VIEWSET    (API = WORKING)
class RoleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]

    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def assign_permissions(self, request, pk=None):
        role = get_object_or_404(Role, pk=pk)
        permissions = request.data.get('permissions', [])

        role.permissions = permissions
        role.save()

        return Response({'detail':  'Permissions assigned successfully.'}, status=status.HTTP_200_OK)

    # def perform_create(self, serializer):
    #     serializer.save()

    # def perform_update(self, serializer):
    #     serializer.save()



