from django.urls import path
from . import views

urlpatterns = [
    # Checkout and payment processing
    path('checkout/', views.checkout, name='checkout'),
    path('create-razorpay-order/', views.create_razorpay_order, name='create-razorpay-order'),
    path('complete-order/', views.complete_order, name='complete-order'),
    
    # Payment status
    path('payment-success/', views.payment_success, name='payment-success'),
    path('payment-failed/', views.payment_failed, name='payment-failed'),
    
    # Webhook for Razorpay
    path('razorpay-webhook/', views.razorpay_webhook, name='razorpay-webhook'),
    path('razorpay-verify/', views.razorpay_verify, name='razorpay-verify'),
]








