from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path
from .views import send_customer_sms
from .views import ExpiringPoliciesView, send_expiry_sms, send_customer_sms

router = DefaultRouter()
router.register('companies', CompanyViewSet)
router.register('users', UserViewSet)
router.register('customers', CustomerViewSet, basename='customer')
router.register('policies', InsurancePolicyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('me/', get_user_info),
    path('register/', RegisterView.as_view(), name='register'),
    path('expiring-policies/', ExpiringPoliciesView.as_view()),
    path('send-expiry-sms/<int:days>/', send_expiry_sms),
    path('send-sms/<int:policy_id>/', send_customer_sms.as_view()),
]

