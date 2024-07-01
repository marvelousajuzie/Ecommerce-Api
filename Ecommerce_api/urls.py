from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from rest_framework_nested.routers import NestedDefaultRouter




router = DefaultRouter()

router.register(r'register', UsersRegisterViewSet,  basename= 'userrgister' ) 
router.register(r'Login', UsersLoginViewSet, basename= 'userlogin')  
router.register(r'Logout', LogoutViewSet, basename='logout')


router.register(r'product', ProductViewSet, basename= 'product') 
product_router = routers.NestedDefaultRouter(router, r'product', lookup = 'product')
product_router.register(r"reviews",ReviewViewSet, basename ='reviews')



router.register(r'basket', CartView, basename='cart') 
cart_router = routers.NestedDefaultRouter(router, r'basket', lookup = 'cart')
cart_router.register(r"items",CartItemView, basename ='cart-items')


router.register(r'order',OrderViewSet, basename= 'order')
order_router = routers.NestedDefaultRouter(router, r'order')
order_router.register(r"shipping", ShippingViewSet, basename= 'shipping' )




router.register(r'category', CategoryViewSet, basename='category')   


router.register(r'role', RoleViewSet, basename='role')  





router.register(r'allUsers', AllUsersView, basename='allusers')  











urlpatterns = [
    path('', include(cart_router.urls)),
    path('', include(product_router.urls)),
    path('', include(order_router.urls)),
    path('', include(router.urls)),
]


