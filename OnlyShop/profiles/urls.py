from django.urls import path, include

from OnlyShop.profiles import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.UserLogIn.as_view(), name='login'),
    path('user-logout/', views.user_logout, name='logout'),
    path('profile/', include([
        path('<int:pk>/edit/', views.ProfileEditView.as_view(), name='profile-edit'),
        path('<int:pk>/view/', views.ProfileDetailView.as_view(), name='profile-details'),
        path('<int:pk>/delete/', views.ProfileDeleteView.as_view(), name='profile-delete'),
        ])),
]
