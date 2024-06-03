from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from rest_framework_nested.routers import NestedDefaultRouter




router = DefaultRouter()

router.register(r'Register', UsersRegisterViewSet,  basename= 'userrgister' )  # USER REGISTER
router.register(r'Login', UsersLoginViewSet, basename= 'userlogin')   # USER LOGIN
router.register(r'Product', ProductViewSet, basename= 'product') 
router.register(r'Category', CategoryViewSet, basename='category')    
router.register(r'Basket', CartView, basename='cart')                   
router.register(r'Order',OrderViewSet, basename= 'ORDER')


router.register(r'userlogout', UserLogoutView, basename= 'userlogout')   # USER LOGOUT


 
# router.register(r'Order', OrderViewSet, basename='order')
# router.register(r'Order/(?P<order_pk>[^/.]+)/items', OrderItemViewSet, basename='orderitem')



cart_router = routers.NestedDefaultRouter(router, r'Basket', lookup = 'cart')
cart_router.register(r"Items",CartItemView, basename ='cart-items')






                         #CUSTOMER REGISTRATION/LOGIN

router.register(r'admincreate',  AdminCreateViewSet, basename='admincreate')   #ADMIN CREATE ROLE



# router.register(r'CartView', CartView, basename= 'CartView')
# router.register(r'AddToCartView', CartItemView, basename= 'AddToCartView')
router.register(r'reviewView', ReviewViewSet, basename= 'reviewView')
# router.register(r'payment', PaymentViewSet, basename= 'payment')
# router.register(r'passwordResetView', PasswordResetRequestView, basename= 'passwordResetView')

urlpatterns = [

    path('', include(router.urls)),
    path('', include(cart_router.urls)),
    # path('AddToCartView/',AddToCartView.as_view({'get': 'post'})),
    # path('payment/', PaymentViewSet.as_view({'get': 'post'})),
    # path('reviewView/',ReviewViewSet.as_view({'get': 'create'})),
]


