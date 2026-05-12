from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # Main Website (Home, Product Detail, etc.)
    path('', include('marketplace.urls')),

    # Authentication (Login, Logout, Password Reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')),
]