from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter




router = DefaultRouter()


router.register(r'adminProductView', AdminProductViewSet, basename= 'product') #ADMIN FOR PRODUCT
router.register(r'ProductView', UserProductViewSet, basename= 'ProductView')  #USER PRODUCT VIEW 
router.register(r'admincategory', AdminCategoryViewSet, basename='category') #ADMIN FOR CATEGORY
router.register(r'userCategory', UsercategoryViewSet, basename= 'Category')                       
router.register(r'UserOrder',OrderViewSet, basename= 'ORDER')
router.register(r'adminorder',AdminOrderView, basename= 'AdminOrderView')
router.register(r'userregister', UsersRegisterViewSet,  basename= 'userrgister' )  # USER REGISTER
router.register(r'userlogin', UsersLoginViewSet, basename= 'userlogin')   # USER LOGIN
router.register(r'userlogout', UserLogoutView, basename= 'userlogout')   # USER LOGOUT


router.register(r'Basket', CartView, basename='CartView')


cart_router = routers.NestedDefaultRouter(router, 'Basket', lookup = 'Basket')
cart_router.register("items",CartItemView, base_name ='cart-items')






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


