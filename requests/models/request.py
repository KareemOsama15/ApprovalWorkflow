from django.db import models


class RequestType(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name_en = models.CharField(unique=True, max_length=50)
    name_ar = models.CharField(unique=True, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.name_en} - {self.name_ar}"


class RequestStatus(models.Model):
    code = models.IntegerField(primary_key=True)
    name_en = models.CharField(unique=True, max_length=50)
    name_ar = models.CharField(unique=True, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.name_en} - {self.name_ar}"


class Request(models.Model):
    type = models.ForeignKey(RequestType, on_delete=models.CASCADE)
    status = models.ForeignKey(RequestStatus, on_delete=models.CASCADE)
    customer = models.ForeignKey(
        "requests.Customer", on_delete=models.CASCADE, null=True, blank=True
    )
    number = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.number} - {self.type}"


class RequestProduct(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    product = models.ForeignKey("requests.Product", on_delete=models.CASCADE)
    asked_quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.request.number} - {self.product.name_en}"


class RequestSequence(models.Model):
    sequence = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
