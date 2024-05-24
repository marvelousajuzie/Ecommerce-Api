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
from django.core.mail import send_mail
from django.template.loader import render_to_string
from Ecommerce import settings
from .view import initial_payment
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken

            



        
                          #SECTION FOR PRODUCTVIEW   # (API= WORKING)
 #For ISADMIN PRODUCTVIEW
class AdminProductViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAdminUser]

    serializer_class = ProductSerializer
    queryset = Product.objects.all()

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


#FOR CUSTOMERS PRODUCTS VIEW
class UserProductViewSet(viewsets.ReadOnlyModelViewSet):      
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_queryset(self):
        return Product.objects.all()
    


                         # SECTION FOR CATEGORY  # (API= WORKING)
# CATEGORY FOR ISADMIN
class AdminCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]

    serializer_class = CategorySerializer()
    queryset = Category.objects.all()

    def list(self, request, *args, **Kwargs): # (API= WORKING)
        category = self.get_queryset()
        serializer = self.serializer_class(category, many= True)
        return Response(serializer.data, status= status.HTTP_200_OK)
    
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

#CUSTOMER CATEGORY
class UsercategoryViewSet(viewsets.ReadOnlyModelViewSet):  #not working
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    # def get_queryset(self):   
    #     return  Category.objects.all()




                 #SECTION FOR ORDER  # (API= WORKING)
# ORDER FOR CUSTOMERS
class OrderViewSet(ModelViewSet):       
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        else:
            return OrderSerializer
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        else:
            return Order.objects.filter(user_id= user)
        
    def create(self, request):   #CUSTOMERS CAN ORDER PRODUCT   #(API= WORKING)
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                with transaction.atomic():
                    order = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#PAYMENT
    # @action(detail= True, methods= ['POST'])
    # def pay(self, request, pk):
    #     order = self.get_object()
    #     amount = order.total_price()
    #     email = request.email
    #     redirect_url = "http://127.0.0.1:9000/confirm/"
    #     return initial_payment(amount, email, redirect_url)


#ORDER HISTORY IS ADMIn
class AdminOrderView(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        return Order.objects.all()
    
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



#PAYMENT HISTORY FOR ISADMIN
# class PaymentView(viewsets.ModelViewSet):
#     serializer_class = PaymentSerializer
#     queryset = Payment.objects.all

#     def get(self, request):
#         payment = self.get_queryset()
#         serializer = self.serializer_class(payment, many= True)
#         return Response(serializer.data, status= status.HTTP_200_OK)
    


    
    
# ALL USERS FOR IS ADMIN
# class CustomUserView(viewsets.ModelViewSet):
#     serializer_class = CustomUserSerializer
#     queryset = CustomUsers.objects.get()

#     def get(self, request):
#         Users = self.get_queryset()
#         serializer = self.serializer_class(Users, many= True)
#         return Response(serializer.data, status= status.HTTP_200_OK)



# # ISADMIN REVIEW
# class ReviewView(viewsets.ModelViewSet):
#     serializer_class = ReviewSerializer
#     queryset = Review.objects.all()
#     def get(self, request):
#         review = self.get_queryset()
#         serializer = self.serializer_class(review)
#         return Response(serializer.data, status= status.HTTP_200_OK)
    
    
    
    


















#CUSTOMER LOGOUT
class UserLogoutView(viewsets.ModelViewSet):
    
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


   
class CartView(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemView(viewsets.ModelViewSet):

    def get_queryset(self):
        return Cartitems.objects.filter(cart_id = self.kwargs["cart_pk"])
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddToCartSerializer
        
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {"cart_id": self.kwargs['cart_pk']}
    
