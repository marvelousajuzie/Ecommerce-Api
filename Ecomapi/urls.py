from django.urls import path, include
from .views import AdminProductViewSet, AdminCategoryViewSet,  AdminCreateViewSet
from .views import UsersRegisterViewSet, UsersLoginViewSet, UserOrderViewSet
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
                                   # FOR ADMIN USERS
router.register(r'adminProductView', AdminProductViewSet, basename= 'product')  #WORKING FOR PRODUCT
router.register(r'admincategoryview', AdminCategoryViewSet, basename='category')    #WORKING FOR CATEGORY
router.register(r'admincreate',  AdminCreateViewSet, basename='admincreate')


                         #CUSTOMER REGISTRATION/LOGIN
router.register(r'userregister', UsersRegisterViewSet,  basename= 'userrgister' )  # USER REGISTER
router.register(r'userlogin', UsersLoginViewSet, basename= 'userlogin')   # USER LOGIN


urlpatterns = [

    path('', include(router.urls)),
    
    path('userOrderView/',UserOrderViewSet.as_view({'get': 'create'})),
    #  path('userProductView/', UserProductViewSet.as_view({'get': 'create'})),
    # path('payment/', PaymentViewSet.as_view({'get': 'post'})),  
]


