from django.urls import path, include
from OnlyShop.main_app import views

urlpatterns = [
    path('<int:pk>/details/', views.ItemDetailView.as_view(), name='item-details'),
    path('<int:pk>/add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('<int:pk>/remove-from-cart/', views.remove_from_cart, name='remove-from-cart'),
    path('add-item/', views.ItemCreateView.as_view(), name='add_item'),
]