from rest_framework import serializers
from .models import Company, User, Customer, InsurancePolicy
from datetime import date, timedelta
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class PolicySerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.full_name', read_only=True)
    customer_phone = serializers.CharField(source='customer.phone', read_only=True)
    company_name = serializers.CharField(source='customer.company.name', read_only=True)

    class Meta:
        model = InsurancePolicy
        fields = '__all__'
        
class RegisterSerializer(serializers.Serializer):
    company_name = serializers.CharField(max_length=255)
    company_address = serializers.CharField()
    company_phone = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        company = Company.objects.create(
            name=validated_data['company_name'],
            address=validated_data['company_address'],
            phone_number=validated_data['company_phone'], 
            service_expiration=date.today() + timedelta(days=365),
        )
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            company=company,
        )
        return user
        
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'address', 'phone_number', 'service_expiration', 'status']  # 👈 Add 'status'

class UserSerializer(serializers.ModelSerializer):
    is_superuser = serializers.SerializerMethodField()
    company = CompanySerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'company', 'is_superuser']

    def get_is_superuser(self, obj):
        return obj.is_superuser

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        extra_kwargs = {
            'company': {'read_only': True}
        }

class InsurancePolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = InsurancePolicy
        fields = '__all__'


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user
        company = getattr(user, 'company', None)

        data['user'] = {
            'id': user.id,
            'username': user.username,
            'is_superuser': user.is_superuser,
            'company': {
                'id': company.id,
                'name': company.name,
                'status': company.status,
                'service_expiration': company.service_expiration,
                'phone_number': company.phone_number,
            } if company else None
        }

        return data

