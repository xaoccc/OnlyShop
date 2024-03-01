from django.urls import path, include
from django.contrib.auth import views as auth_views
from OnlyShop.profiles import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.UserLogIn.as_view(), name='login'),
    # path('', views.user_logout, name='logout'),
    # path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]