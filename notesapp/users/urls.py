from django.urls import path 
from .views import UserViewSet
  
urlpatterns = [ 
    path("signup/", UserViewSet.as_view({'post': 'create'}), name="sign-up"),
    path("login/", UserViewSet.as_view({'get': 'retrieve'}), name="login-up"),
] 