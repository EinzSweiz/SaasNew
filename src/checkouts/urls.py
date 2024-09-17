from django.urls import path 
from . import views

app_name = 'checkouts'

urlpatterns = [
    path('start/', views.checkout_redirect_view, name='checkout_redirect'),
    path('sub-price/<int:price_id>/', views.subscription_price_redirect_view, name='sub_price_checkout'),
    path('success/', views.checkout_finalize_view, name='checkout_success')

]