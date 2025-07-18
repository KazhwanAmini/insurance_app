from datetime import date, timedelta
import os
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Company, User, Customer, InsurancePolicy,SMSLog
from .serializers import (
    CompanySerializer,
    UserSerializer,
    CustomerSerializer,
    InsurancePolicySerializer,
    PolicySerializer,
    RegisterSerializer,
    CustomTokenObtainPairSerializer,
    SMSLogSerializer
)
from utils.sms import convert_to_persian, send_sms


# ✅ Get only expiring policies for logged-in user's company
class ExpiringPoliciesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = date.today()
        upcoming = today + timedelta(days=10)
        user_company = request.user.company

        policies = InsurancePolicy.objects.filter(
            end_date__range=[today, upcoming],
            customer__company=user_company
        )

        serializer = PolicySerializer(policies, many=True)
        return Response(serializer.data)


# ✅ Bulk send SMS for policies expiring in X days (1, 5, 10)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_expiry_sms(request, days):
    today = date.today()
    target_date = today + timedelta(days=int(days))
    user_company = request.user.company

    policies = InsurancePolicy.objects.filter(
        end_date=target_date,
        customer__company=user_company
    )

    for policy in policies:
        customer = policy.customer
        policy_type = os.getenv(policy.policy_type)
        persian_date = convert_to_persian(policy.end_date)
        company = customer.company

        message = f"{user_company.name} - {customer.full_name} عزیز، بیمه {policy_type} شما در تاریخ {persian_date} منقضی می‌شود. لطفا برای تمدید اقدام کنید.\n{company.name}\n{company.phone_number}"
       
        send_sms(customer.phone, message,policy.company)

    return Response({'status': 'ok', 'count': policies.count()})


# ✅ Send SMS to a single customer for a selected policy
class send_customer_sms(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, policy_id):
        try:
            policy = InsurancePolicy.objects.get(id=policy_id)
            policy_type = os.getenv(policy.policy_type)
            persian_date = convert_to_persian(policy.end_date)
            customer = policy.customer
            company = customer.company
            phone = customer.phone
            message = f"{customer.full_name} عزیز، بیمه‌نامه {policy_type} شما در تاریخ {persian_date} منقضی می‌شود. لطفاً برای تمدید اقدام کنید. \n{company.name}\n{company.phone_number}"
            result = send_sms(phone, message,customer.company)
            return Response({"status": "sent", "result": result}, status=status.HTTP_200_OK)
        except InsurancePolicy.DoesNotExist:
            return Response({"error": "Policy not found"}, status=status.HTTP_404_NOT_FOUND)


# ✅ Register endpoint
class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ CRUD for Companies
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]


# ✅ CRUD for Users
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]


# ✅ CRUD for Customers, scoped by company
class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Customer.objects.none()
        user = self.request.user
        if user.is_superuser:
            return Customer.objects.all()
        return Customer.objects.filter(company=user.company)

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)


# ✅ CRUD for Insurance Policies, scoped by customer.company
class InsurancePolicyViewSet(viewsets.ModelViewSet):
    serializer_class = InsurancePolicySerializer
    permission_classes = [IsAuthenticated]
    queryset = InsurancePolicy.objects.all()  # ✅ Add this line

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return InsurancePolicy.objects.none()
        user = self.request.user
        if user.is_superuser:
            return InsurancePolicy.objects.all()
        return InsurancePolicy.objects.filter(customer__company=user.company)


# ✅ Get current user info
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


    
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def company_profile(request):
    company = request.user.company
    if request.method == 'GET':
        return Response(CompanySerializer(company).data)
    elif request.method == 'PUT':
        serializer = CompanySerializer(company, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sms_logs(request):
    company = request.user.company
    logs = SMSLog.objects.filter(company=company).order_by('-sent_at')
    return Response(SMSLogSerializer(logs, many=True).data)