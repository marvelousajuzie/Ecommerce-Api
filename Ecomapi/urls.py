from django.urls import path, include
from .views import ProductViewSet, UsersRegisterViewSet, UsersLoginViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'product', ProductViewSet, basename= 'product')  #WORKING FOR PRODUCT
router.register(r'userregister', UsersRegisterViewSet,  basename= 'userrgister' )  # USER REGISTER
router.register(r'userlogin', UsersLoginViewSet, basename= 'userlogin')   # USER LOGIN


urlpatterns = [

    path('', include(router.urls)),
    
]
