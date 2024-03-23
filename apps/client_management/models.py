from django.db import models
from django.contrib.auth.models import User


class ClientData(models.Model):
    COMPANY_STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    company_name = models.CharField(max_length=255, null=False)
    company_id_number = models.CharField(max_length=255, null=True, blank=True)
    company_type = models.CharField(max_length=255, null=True, blank=True)
    company_nationality = models.CharField(max_length=255, null=True, blank=True)
    business_sector = models.CharField(max_length=255, null=True, blank=True)
    primary_contact = models.CharField(max_length=255, null=True, blank=True)
    primary_email = models.EmailField(max_length=255, null=True, blank=True)
    representatives = models.IntegerField(null=True, blank=True)
    website = models.URLField(max_length=255, null=True, blank=True)
    relationship_status = models.CharField(max_length=8, choices=COMPANY_STATUS_CHOICES, default='Active')
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.company_name



class UserCompany(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(ClientData, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.company.company_name}'