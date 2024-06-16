from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from rest_framework_nested.routers import NestedDefaultRouter




router = DefaultRouter()

router.register(r'Register', UsersRegisterViewSet,  basename= 'userrgister' ) 
router.register(r'Login', UsersLoginViewSet, basename= 'userlogin')  
router.register(r'Logout', LogoutViewSet, basename='logout')


router.register(r'Product', ProductViewSet, basename= 'product') 
product_router = routers.NestedDefaultRouter(router, r'Product', lookup = 'product')
product_router.register(r"reviews",ReviewViewSet, basename ='reviews')


router.register(r'Basket', CartView, basename='cart') 
cart_router = routers.NestedDefaultRouter(router, r'Basket', lookup = 'cart')
cart_router.register(r"Items",CartItemView, basename ='cart-items')


router.register(r'Order',OrderViewSet, basename= 'order')
order_router = routers.NestedDefaultRouter(router, r'Order')
order_router.register(r"shipping", ShippingViewSet, basename= 'shipping' )




router.register(r'Category', CategoryViewSet, basename='category')   
# router.register(r'shipping', ShippingViewSet, basename='shipping')   













router.register(r'passwordreset',PasswordResetView, basename= 'password')




urlpatterns = [

    path('', include(router.urls)),
    path('', include(cart_router.urls)),
    path('', include(product_router.urls)),
    path('', include(order_router.urls)),
  
]


