from django.urls import path, include
from OnlyShop.profiles import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]