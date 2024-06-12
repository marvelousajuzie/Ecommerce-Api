from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from rest_framework_nested.routers import NestedDefaultRouter




router = DefaultRouter()

router.register(r'Register', UsersRegisterViewSet,  basename= 'userrgister' )  # USER REGISTER
router.register(r'Login', UsersLoginViewSet, basename= 'userlogin')   # USER LOGIN
router.register(r'Category', CategoryViewSet, basename='category')   
router.register(r'shipping', ShippingViewSet, basename='shipping')   


router.register(r'Product', ProductViewSet, basename= 'product') 
product_router = routers.NestedDefaultRouter(router, r'Product', lookup = 'product')
product_router.register(r"reviews",ReviewViewSet, basename ='reviews')




router.register(r'Basket', CartView, basename='cart') 
cart_router = routers.NestedDefaultRouter(router, r'Basket', lookup = 'cart')
cart_router.register(r"Items",CartItemView, basename ='cart-items')



router.register(r'Order',OrderViewSet, basename= 'ORDER')
# order_router = routers.NestedDefaultRouter(router, r'Order', Lookup = 'ORDER')
# order_router.register(r"Items", )


router.register(r'passwordreset',PasswordResetView, basename= 'password')

router.register(r'userlogout', UserLogoutView, basename= 'userlogout')   # USER LOGOUT



 










                         #CUSTOMER REGISTRATION/LOGIN

router.register(r'admincreate',  AdminCreateViewSet, basename='admincreate')   #ADMIN CREATE ROLE



# router.register(r'reviewView', ReviewViewSet, basename= 'reviewView')
# router.register(r'payment', PaymentViewSet, basename= 'payment')
# router.register(r'passwordResetView', PasswordResetRequestView, basename= 'passwordResetView')

urlpatterns = [

    path('', include(router.urls)),
    path('', include(cart_router.urls)),
     path('', include(product_router.urls)),
    # path('reviewView/',ReviewViewSet.as_view({'get': 'create'})),
]


