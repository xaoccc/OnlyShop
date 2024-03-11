from django.urls import path, include
from OnlyShop.main_app import views as product_views
from OnlyShop.profiles import views as profile_views

urlpatterns = [
    path('<int:pk>/item-details/', product_views.ItemDetailView.as_view(), name='item-details'),
    path('<int:pk>/item-edit/', product_views.ItemEditView.as_view(), name='item-edit'),
    path('<int:pk>/item-delete/', product_views.ItemDeleteView.as_view(), name='item-delete'),
    path('<int:pk>/add-to-cart/', product_views.add_to_cart, name='add-to-cart'),
    path('<int:pk>/remove-from-cart/', product_views.remove_from_cart, name='remove-from-cart'),
    path('add-item/', product_views.ItemCreateView.as_view(), name='add_item'),
    path('checkout/', product_views.OrderSummaryView.as_view(), name='checkout'),
]