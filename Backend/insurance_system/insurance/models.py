from django.contrib.auth.models import AbstractUser
from django.db import models

class Company(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('deactivated', 'Deactivated'),
    ]

    name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    service_expiration = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # 👈 Add this line
    sms_credit = models.PositiveIntegerField(default=100000)

    def __str__(self):
        return self.name

class CreditTopUpRequest(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    card_last4 = models.CharField(max_length=4)
    amount = models.PositiveIntegerField()
    tracking_code = models.CharField(max_length=100)
    payment_date = models.DateField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    

class SMSLog(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    recipient = models.CharField(max_length=20)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

class User(AbstractUser):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField()
    is_superadmin = models.BooleanField(default=False) 

class Customer(models.Model):
    full_name = models.CharField(max_length=100)
    national_id = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

class InsurancePolicy(models.Model):
    POLICY_TYPES = [
        ('Car', 'Car'),
        ('Fire', 'Fire'),
        ('Life', 'Life'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    policy_type = models.CharField(max_length=10, choices=POLICY_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    details = models.TextField()
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)