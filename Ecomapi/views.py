from django.shortcuts import render, get_object_or_404
from .serializer import ProductSerializer, UsersRegisterSerializer,UsersLoginSerializer, OrderSerializer, PaymentSerializer, AdminCreateSerializer, CategorySerializer, CustomUserSerializer, ReviewSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Order, Payment, CustomUsers, Category, Review



 #For ISADMIN PRODUCTVIEW
class ProductViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAdminUser]

    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get(self, request):       #IS ADMIN CAN GET ALL PRODUCTS   (API= WORKING)
        product = self.get_queryset()
        serializer = self.serializer_class(product, many= True)
        return Response(serializer.data, status= status.HTTP_200_OK)
    

    def post(self, request):                   #IS ADMIN CAN POST   (API= WORKING)
        serializer = self.serializer_class(data= request.data)
        if serializer.is_valid(raise_exception= True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def put(self, request, product_id):    #IS ADMIN CAN UPDATE   (API= WORKING)
        query_set = get_object_or_404(Product, product_id= product_id)
        serializer = self.serializer_class(query_set, data=request.data, partial= True)
        if serializer.is_valid(raise_exception= True):
            serializer.save()
            return Response({'message': 'Updated Successfully'}, status= status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, product_id):            # IS ADMIN CAN DELETE    (API= WORKING)
        product = get_object_or_404( Product, product_id= product_id)
        product.delete()
        return Response({'message': 'Product Deleted Successfully'}, status= status.HTTP_200_OK)
    

    

# ORDER FOR IsAdminUser
class OrderView(viewsets.ModelViewSet):
    # permission_classes = [IsAdminUser]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get(self, request):         #IS ADMIN USER CAN  GET ALL ORDERS
        order = self.get_queryset()
        serializer = self.serializer_class(order, many= True)
        return Response(serializer.save)
    

#PAYMENT HISTORY FOR ISADMIN
class PaymentView(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all

    def get(self, request):
        payment = self.get_queryset()
        serializer = self.serializer_class(payment, many= True)
        return Response(serializer.data, status= status.HTTP_200_OK)
    

#IS ADMIN CREATE VIEW   
class AdminCreateView(viewsets.ModelViewSet):
    queryset = CustomUsers.objects.all()
    serializer_class = AdminCreateSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.IsAdminUser()]  # Only allow superusers to create users
        return [permissions.IsAuthenticated()]
    


      #CATEGORY SECTION FOR ADMIN AND CUSTOMER

# CATEGORY FOR ISADMIN
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def list(self, request):         # IS ADMIN CAN GET ALL CATEGORY  (API= WORKING)
        category = self.get_queryset()
        serializer = self.serializer_class(category, many= True)
        return Response(serializer.data, status= status.HTTP_200_OK)
    
    def post(self, request):          #IS ADMIN CAN ADD NEW CATEGORY   (API= WORKING)
        serializer = self.serializer_class(data= request.data)
        if serializer.is_valid(raise_exception= True):
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, category_id):      #IS ADMIN CAN UPDATE CATEGORY   (API= WORKING)
        query_set = get_object_or_404( Category, category_id = category_id)
        serializer = self.serializer_class(query_set, data= request.data)
        if serializer.is_valid(raise_exception= True):
            serializer.save()
            return Response(serializer.data, status= status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, category_id):          #IS ADMIN CAN DELETE CATEGORY     (API= WORKING)    
        query_set = get_object_or_404(Category, category_id= category_id)
        query_set.delete()
        return Response({'Deleted Sucessfully'}, status= status.HTTP_200_OK)
    
    
# ALL USERS FOR IS ADMIN
# class CustomUserView(viewsets.ModelViewSet):
#     serializer_class = CustomUserSerializer
#     queryset = CustomUsers.objects.get()

#     def get(self, request):
#         Users = self.get_queryset()
#         serializer = self.serializer_class(Users, many= True)
#         return Response(serializer.data, status= status.HTTP_200_OK)



# ISADMIN REVIEW
class ReviewView(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    def get(self, request):
        review = self.get_queryset()
        serializer = self.serializer_class(review)
        return Response(serializer.data, status= status.HTTP_200_OK)
    
    
    
    














# # #FOR CUSTOMERS PRODUCTS VIEW
# class ProductView(GenericAPIView):      

#     serializer_class = ProductSerializer
#     queryset = Product.objects.all()


#     def get(self, request):            #CUSTOMERS CAN GET All PRODUCT    #(API= WORKING)
#         product = self.get_queryset()
#         serializer = self.serializer_class(product, many= True)
#         return Response(serializer.data, status= status.HTTP_200_OK)
    

#     def get(self, request, product_id):         #CUSTOMERS CAN GET SINGLE PRODUCT    #(API= WORKING)
#         product = get_object_or_404(Product, product_id= product_id)
#         serializer= self.serializer_class(product, many= False)
#         return Response(serializer.data, status= status.HTTP_200_OK)



# CUSTOMER REGISTRATION
class UsersRegisterViewSet(viewsets.ModelViewSet):
    serializer_class = UsersRegisterSerializer
    def get_queryset(self):
        return []

    def create(self, request):                                     #(API= WORKING)
        serializer = self.serializer_class(data= request.data)
        if serializer.is_valid(raise_exception= True):
            serializer.save()
            user = serializer.data
            return Response({'data': user}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


#CUSTOMER LOGIN
class UsersLoginViewSet(viewsets.ModelViewSet):

    serializer_class = UsersLoginSerializer

    def get_queryset(self):
        return []

    def post(self, request):                                 #(API= WORKING)
        serializer = self.serializer_class(data= request.data)
        if serializer.is_valid():
            user= serializer.validated_data['CustomUsers']
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token), 'messages': 'Logged In Successfully',
            }, status= status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
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
    

# ORDER FOR CUSTOMERS
class OrderView(viewsets.ModelViewSet):       
    # permission_classes = [IsAuthenticated]

    serializer_class = OrderSerializer

    def post(self, request):             # CUSTOMERS TO ORDER PRODUCT
        serializer = self.serializer_class(data= request.data)
        if serializer.is_valid():
            product_data = serializer.validated_data.get('Product')
            total_price = sum(Product.price for Product in product_data)
            shipping_address = serializer.validated_data.get('shipping_address')
            payment_method = serializer.validated_data.get('payment method')
            user_id = request.user
            order = Order.objects.create(
                user_id = user_id,
                total_price = total_price,
                shipping_address = shipping_address,
                payment_method = payment_method
            )
            order.products.add(*product_data)

            for product in product_data:
                product.stock_quantity =-1
                product.save()
            return Response({'messages': 'Your Order Has Been Placed'}, status= status.HTTP_200_OK)
        return Response({'messages': 'Order Has Not Been Placed'}, status= status.HTTP_400_BAD_REQUEST)
    





#PAYMENT FOR CUSTOMERS
class PaymentView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    serializer_class = PaymentSerializer

    def post(self, request):
        serializer = self.serializer_class(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'messages': 'Payment sucessfully'}, status= status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    

#CUSTOMER CATEGORY
class categoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get(self, request):
        category = self.get_queryset()
        serializer = self.serializer_class(category, many= True)
        return Response(serializer.data, status= status.HTTP_200_OK)
    



