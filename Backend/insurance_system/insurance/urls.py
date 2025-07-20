from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path
from .views import send_customer_sms,CustomTokenObtainPairView
from .views import ExpiringPoliciesView, send_expiry_sms, send_customer_sms, company_profile, sms_logs, CreditTopUpCreateView, CreditTopUpListView, CreditTopUpVerifyView

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
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('company/profile/', company_profile),
    path('company/sms-logs/', sms_logs),
    path('credit-topup/', CreditTopUpCreateView.as_view()),
    path('credit-topup/admin/', CreditTopUpListView.as_view()),
    path('credit-topup/verify/<int:pk>/', CreditTopUpVerifyView.as_view()),

]

