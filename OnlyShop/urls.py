
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/', include('allauth.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('product/', include('OnlyShop.main_app.urls')),
    path('', include('OnlyShop.profiles.urls')),
]
