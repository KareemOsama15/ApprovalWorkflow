from django.contrib import admin
from requests.models import (
    RequestType,
    RequestStatus,
    RequestProduct,
    CustomerCategory,
    Request,
    ApprovedProduct,
    Product,
    CommitteeForm,
    TechnicalForm,
    Customer,
    RequestSequence,
)


@admin.register(RequestProduct)
class RequestProductAdmin(admin.ModelAdmin):
    list_display = ["request", "product", "asked_quantity"]
    search_fields = ["request__number"]


@admin.register(CustomerCategory)
class CustomerCategoryAdmin(admin.ModelAdmin):
    list_display = ["code", "name_en", "name_ar"]
    list_filter = ["name_en"]


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["id_number", "name_en", "name_ar", "category"]
    search_fields = ["id_number", "name_en", "name_ar", "category__name_en"]
    list_filter = ["category__name_en"]


@admin.register(RequestSequence)
class RequestSequenceAdmin(admin.ModelAdmin):
    list_display = ["sequence"]


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ["number", "type", "status", "customer", "created_at"]
    search_fields = ["number", "customer__name_en", "customer__name_ar"]
    list_filter = ["type", "status"]


@admin.register(ApprovedProduct)
class ApprovedProductAdmin(admin.ModelAdmin):
    list_display = ["customer", "product", "quantity"]
    search_fields = ["customer__name_en", "customer__name_ar", "product__code"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["code", "name_en", "name_ar"]
    search_fields = ["code", "name_en", "name_ar"]


@admin.register(CommitteeForm)
class CommitteeFormAdmin(admin.ModelAdmin):
    list_display = ["number", "request", "assigned_to", "created_at"]
    search_fields = ["number", "request__number", "assigned_to__username"]


@admin.register(TechnicalForm)
class TechnicalFormAdmin(admin.ModelAdmin):
    list_display = ["number", "request", "assigned_to", "created_at"]
    search_fields = ["number", "request__number", "assigned_to__username"]


@admin.register(RequestType)
class RequestTypeAdmin(admin.ModelAdmin):
    list_display = ["code", "name_en", "name_ar"]
    list_filter = ["name_en"]


@admin.register(RequestStatus)
class RequestStatusAdmin(admin.ModelAdmin):
    list_display = ["code", "name_en", "name_ar"]
    list_filter = ["name_en"]
