from django.db import models


class CustomerCategory(models.Model):
    code = models.IntegerField(primary_key=True)
    name_en = models.CharField(unique=True, max_length=20)
    name_ar = models.CharField(unique=True, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.name_en} - {self.name_ar}"


class Customer(models.Model):
    name_en = models.CharField(max_length=100, blank=True, null=True)
    name_ar = models.CharField(max_length=100, blank=True, null=True)
    id_number = models.CharField(unique=True, max_length=20)
    category = models.ForeignKey(CustomerCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.name_en} - {self.category.name_en}"


class ApprovedProduct(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey("requests.Product", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.customer.id_number} - {self.product.code}"
