from django.urls import path

from OnlyShop.order import views

urlpatterns = [
    path('', views.AllOrdersView.as_view(), name='all_orders'),
    path('<int:pk>/', views.OrderDetailsView.as_view(), name='order_details'),
    path('completed/', views.OrderCompleteView.as_view(), name='order_completed'),
]