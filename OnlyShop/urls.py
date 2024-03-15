
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/', include('allauth.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('item/', include('OnlyShop.main_app.urls')),
    path('', include('OnlyShop.profiles.urls')),
    # path('order/', include('OnlyShop.order.urls')),
]
