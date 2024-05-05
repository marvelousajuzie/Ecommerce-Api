from django.urls import path, include
from .views import AdminProductViewSet, AdminCategoryViewSet,  AdminCreateViewSet
from .views import UsersRegisterViewSet, UsersLoginViewSet, UserOrderViewSet, UserProductViewSet
from .views import  UsercategoryViewSet, ReviewViewSet, IsadminOrderViewSet, PaymentViewSet
from .views import AddToCartView
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
                                   # FOR ADMIN USERS
router.register(r'adminProductView', AdminProductViewSet, basename= 'product')  #ADMIN FOR PRODUCT
router.register(r'admincategoryview', AdminCategoryViewSet, basename='category')    #ADMIN FOR CATEGORY
router.register(r'admincreate',  AdminCreateViewSet, basename='admincreate')  #ADMIN CREATE ROLE
router.register(r'IsadminOrder',  IsadminOrderViewSet, basename='IsadminOrder')  #ADMIN GET ORDER HISTROY



                         #CUSTOMER REGISTRATION/LOGIN
router.register(r'userregister', UsersRegisterViewSet,  basename= 'userrgister' )  # USER REGISTER
router.register(r'userlogin', UsersLoginViewSet, basename= 'userlogin')   # USER LOGIN
router.register(r'userProductView', UserProductViewSet, basename= 'userProductView')  #USER PRODUCT VIEW 
router.register(r'userCategoryView', UsercategoryViewSet, basename= 'userCategoryView')
router.register(r'userOrderView',UserOrderViewSet, basename= 'userOrderView')




router.register(r'AddToCartView', AddToCartView, basename= 'AddToCartView')
router.register(r'reviewView', ReviewViewSet, basename= 'reviewView')
router.register(r'payment', PaymentViewSet, basename= 'payment')

urlpatterns = [

    path('', include(router.urls)),
    # path('AddToCartView/',AddToCartView.as_view({'get': 'post'})),
    # path('payment/', PaymentViewSet.as_view({'get': 'post'})),
    # path('reviewView/',ReviewViewSet.as_view({'get': 'create'})),
]


