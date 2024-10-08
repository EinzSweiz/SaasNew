"""
URL configuration for cfehome project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from auth import urls as auth_urls
from profiles import urls as profile_urls
from subscriptions import urls as subscriptions_urls
from checkouts import urls as checkouts_urls
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view_page, name='home'),
    path('user/', include(auth_urls, namespace='user')),
    path('accounts/', include('allauth.urls')),
    path('protected/', views.pw_protected_view, name='protected'),
    path('protected/user-only/', views.user_only_view, name='user_only'),
    path('protected/staff-only/', views.staff_only_view , name='staff_only'),
    path('profiles/', include(profile_urls, namespace='profiles')),
    path('checkout/', include(checkouts_urls, namespace='checkouts')),
    path('subscriptions/', include(subscriptions_urls, namespace='subscriptions'))

]
