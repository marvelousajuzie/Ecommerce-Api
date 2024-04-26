from django.urls import path, include
from .views import ProductViewSet, UsersRegisterViewSet, UsersLoginViewSet, CategoryViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'product', ProductViewSet, basename= 'product')  #WORKING FOR PRODUCT


router.register(r'userregister', UsersRegisterViewSet,  basename= 'userrgister' )  # USER REGISTER
router.register(r'userlogin', UsersLoginViewSet, basename= 'userlogin')   # USER LOGIN


urlpatterns = [

    path('', include(router.urls)),


    path('getcategory/', CategoryViewSet.as_view({'get': 'list'})),
    path('postcategory/', CategoryViewSet.as_view({'get': 'post'})),
    path('updatecategory/<uuid:category_id>/', CategoryViewSet.as_view({'get': 'put'})),
    path('deletecategory/<uuid:category_id>/', CategoryViewSet.as_view({'get': 'delete'})),

]