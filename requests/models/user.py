from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.TextChoices):
    # Customers
    BENEFICIARY = "beneficiary", "Beneficiary"
    DIRECT = "direct", "Direct"
    DISTRIBUTOR = "distributor", "Distributor"
    MULTI_BRANCH = "multi_branch", "Multi Branch"

    # Users
    ADMIN = "admin", "Admin"
    BRANCH_MANAGER = "branch_manager", "Branch Manager"
    SALES_MANAGER = "sales_manager", "Sales Manager"
    CEO = "ceo", "CEO"
    COMMITTEE_MEMBER = "committee_member", "Committee Member"
    TECHNICAL_MEMBER = "technical_member", "Technical Member"
    VIEWER = "viewer", "Viewer"


class User(AbstractUser):
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.VIEWER)
    email = models.EmailField(unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.username} - {self.role}"
