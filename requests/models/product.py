from django.db import models


class Product(models.Model):
    code = models.IntegerField(primary_key=True)
    name_en = models.CharField(unique=True, max_length=50)
    name_ar = models.CharField(unique=True, max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.name_en} - {self.name_ar}"
