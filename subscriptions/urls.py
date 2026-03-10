from django.urls import path

from .views import PackageView, SubscriptionView

urlpatterns = [
    path('packages/', PackageView.as_view(), name='packages'),
    path('subscriptions/', SubscriptionView.as_view(), name='subscriptions'),
    
]