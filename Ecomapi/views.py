from django.shortcuts import render, get_object_or_404
from .serializer import ProductSerializer, UsersRegisterSerializer,UsersLoginSerializer, OrderSerializer, PaymentSerializer, CategorySerializer, CustomUserSerializer, ReviewSerializer
from .serializer import AdminCreateSerializer, CartSerializer, PasswordResetSerializer
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from datetime import datetime, timedelta
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.core.mail import send_mail
from django.template.loader import render_to_string
from Ecommerce import settings
from .models import Product, Order, Payment, CustomUsers, Category, Review, Cart

            

                          #SECTION FOR PRODUCTVIEW(IS ADMIN)
 #For ISADMIN PRODUCTVIEW
class AdminProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]

    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get(self, request, *args, **Kwargs):       #IS ADMIN CAN GET ALL PRODUCTS   (API= WORKING)
        product = self.get_queryset()
        serializer = self.serializer_class(product, many= True)
        return Response(serializer.data, status= status.HTTP_200_OK)
    

    def post(self, request, *args, **Kwargs):                   #IS ADMIN CAN POST   (API= WORKING)
        serializer = self.serializer_class(data= request.data)
        if serializer.is_valid(raise_exception= True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def put(self, request, product_id, *args, **Kwargs):    #IS ADMIN CAN UPDATE   (API= WORKING)
        query_set = get_object_or_404(Product, product_id= product_id)
        serializer = self.serializer_class(query_set, data=request.data, partial= True)
        if serializer.is_valid(raise_exception= True):
            serializer.save()
            return Response({'message': 'Updated Successfully'}, status= status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, product_id, *args, **Kwargs):            # IS ADMIN CAN DELETE    (API= WORKING)
        product = get_object_or_404( Product, product_id= product_id)
        product.delete()
        return Response({'message': 'Product Deleted Successfully'}, status= status.HTTP_200_OK)
    


                         #CATEGORY SECTION (IS ADMIN)
# CATEGORY FOR ISADMIN
class AdminCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]

    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def list(self, request, *args, **Kwargs):         # IS ADMIN CAN GET ALL CATEGORY  (API= WORKING)
        category = self.get_queryset()
        serializer = self.serializer_class(category, many= True)
        return Response(serializer.data, status= status.HTTP_200_OK)
    
    def post(self, request, *args, **Kwargs):          #IS ADMIN CAN ADD NEW CATEGORY   (API= WORKING)
        serializer = self.serializer_class(data= request.data)
        if serializer.is_valid(raise_exception= True):
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, category_id, *args, **Kwargs):      #IS ADMIN CAN UPDATE CATEGORY   (API= WORKING)
        query_set = get_object_or_404( Category, category_id = category_id)
        serializer = self.serializer_class(query_set, data= request.data)
        if serializer.is_valid(raise_exception= True):
            serializer.save()
            return Response(serializer.data, status= status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, category_id, *args, **Kwargs):          #IS ADMIN CAN DELETE CATEGORY     (API= WORKING)    
        query_set = get_object_or_404(Category, category_id= category_id)
        query_set.delete()
        return Response({'Deleted Sucessfully'}, status= status.HTTP_200_OK)
    

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

    




# ORDER HISTORY FOR IsAdminUser
class IsadminOrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get(self, request):         #IS ADMIN USER CAN  GET ALL ORDERS    #(API= WORKING)
        order = self.get_queryset()
        serializer = self.serializer_class(order, many= True)
        return Response(serializer.data)
    



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
    
    
    
    









                               #CUSTOMER  SECTION


                     #AUTHENTICATION          
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

    def create(self, request, *args, **Kwargs):                                 #(API= WORKING) 
        serializer = self.serializer_class(data= request.data)
        if serializer.is_valid():
            user= serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token), 'messages': 'Logged In Successfully',
            }, status= status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    # def create_and_store(user):
    #     refresh = RefreshToken.for_user(user)
    #     RefreshToken.objects.create(
    #         user= user,
    #         refresh_token = str(refresh),
    #         valid_until=datetime.fromtimestamp(refresh['exp']),
    #     )
    #     return refresh


class PasswordResetRequestView(viewsets.ModelViewSet):

    serializer_class =  PasswordResetSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data= request.data)
        if serializer.is_valid(raise_exception= True):
            email = serializer.validated_data['email']
            user_qs = CustomUsers.objects.filter(email= email)
            if user_qs.exists():
                user = user_qs.first()
                # Generate JWT token
                token = AccessToken.for_user = user
                 # Set token expiration time
                token ['exp'] = datetime.utcnow() + timedelta(hours =1)
                # Encode user ID for URL
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = str(token)
                # Send email with password reset link
                reset_link = f"{settings.FRONTEND_URL}/password-reset/{uidb64}/{token}/"
                send_mail(
                    'Password Reset',
                    f'Click the following link to reset your password: {reset_link}',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                return Response({'message': 'Password reset email sent'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'User with this email does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PasswordResetConfirmView(viewsets.ModelViewSet):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            uidb64 = serializer.validated_data['uidb64']
            token = serializer.validated_data['token']
            try:
                # Decode user ID from URL
                uid = force_text(urlsafe_base64_decode(uidb64))
                user = CustomUsers.objects.get(pk=uid)
                # Decode token
                token = AccessToken(token)
                # Validate token
                if token['user_id'] == str(user.pk) and not token.is_expired():
                    # Set new password
                    password = serializer.validated_data['password']
                    user.set_password(password)
                    user.save()
                    return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid token or token expired'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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









               # MANAGE PRODUCTS

 #FOR CUSTOMERS PRODUCTS VIEW
class UserProductViewSet(viewsets.ModelViewSet):      
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


    def get(self, request):            #CUSTOMERS CAN GET All PRODUCT    #(API= WORKING)
        product = self.get_queryset()
        serializer = self.serializer_class(product, many= True)
        return Response(serializer.data, status= status.HTTP_200_OK)
    

    def get(self, request, product_id):         #CUSTOMERS CAN GET SINGLE PRODUCT #(API= WORKING)        product = get_object_or_404(Product, product_id= product_id)
        serializer= self.serializer_class(product_id, many= False)
        return Response(serializer.data, status= status.HTTP_200_OK)
    

#CUSTOMER CATEGORY
class UsercategoryViewSet(viewsets.ModelViewSet):  
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get(self, request):             #CUSTOMERS CAN GET All CATEGORY   #(API= WORKING)
        category = self.get_queryset()
        serializer = self.serializer_class(category, many= True)
        return Response(serializer.data, status= status.HTTP_200_OK)
    
    def get(self, request, category_id):      #CUSTOMERS CAN GET SINGLE PRODUCT    #(API= WORKING)
        serializer = self.serializer_class(category_id, many= False)
        return Response(serializer.data, status= status.HTTP_200_OK)
    

# ORDER FOR CUSTOMERS
class UserOrderViewSet(viewsets.ModelViewSet):       
    permission_classes = [IsAuthenticated]

    serializer_class = OrderSerializer
    queryset = Order.objects.all()


    def create(self, request, *args, **kwargs):   #CUSTOMERS CAN ORDER PRODUCT   #(API= WORKING)
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                with transaction.atomic():
                    order = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

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





    




#PAYMENT FOR CUSTOMERS
class PaymentViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]

    serializer_class = PaymentSerializer

    def get_queryset(self):
        return []

    def create(self, request):
        serializer = self.serializer_class(data= request.data)
        serializer.is_valid(raise_exception= True)
        self.perform_create(serializer)
        payment_instance = serializer.instance
        payment_instance.payment_status = 'completed'
        payment_instance.save()

        subject = 'Payment Confirmation'
        message = render_to_string('payment_confirm_email.html', {'payment': payment_instance})
        recipient = payment_instance.user_id.email
        sender = 'Chizurummarvelous14@gmail.com'
        send_mail(subject, message, sender, [recipient])
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)



class AddToCartView(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    query_set = Cart.objects.all()

    def get_queryset(self):
        return []
    
    @action(detail= True, methods= ['post'])
    def add_product(self, request, pk= None):
        cart = self.get_object()
        product_id = request.data.get('product_id')
        try:
            products = Product.objects.get(id = product_id)
            cart.product.add('products')
            cart.total_price += products.price
            cart.save()
            return Response({'messages': 'Item Successfully Added To Cart'}, status= status.HTTP_200_OK)
        except:
            return Response({'messages': 'Item Not Found'}, status= status.HTTP_404_NOT_FOUND)
    

    # @action(detail=True, methods=['post'])
    # def remove_product(self, request):
    #     cart = self.get_object()
    #     product_id = request.data.get('product_id')
    #     try:
    #         product = Product.objects.get(id = product_id)
    #         cart.product.remove('product')
    #         cart.total_price -= product.price
    #         cart.save()
    #         return Response({'messages': 'Item Removed'}, status= status.HTTP_200_OK)
    #     except:
    #         return Response({'messages': 'Item Not Found'}, status= status.HTTP_404_NOT_FOUND)
        



