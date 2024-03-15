from django.urls import path

from OnlyShop.order import views

urlpatterns = [
    path('', views.AllOrdersView.as_view(), name='all_orders'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order_details'),
]