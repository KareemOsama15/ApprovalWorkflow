from django.contrib import admin
from workflow.models import Action, Transition, ApprovelWorkflow


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ["type", "name_en", "name_ar"]
    list_filter = ["name_en"]


@admin.register(Transition)
class TransitionAdmin(admin.ModelAdmin):
    list_display = [
        "workflow",
        "from_status",
        "to_status",
        "action",
        "is_final",
    ]
    search_fields = ["workflow", "from_status", "to_status", "action", "is_final"]
    list_filter = ["workflow__request_type", "from_status", "action", "is_final"]


@admin.register(ApprovelWorkflow)
class ApprovelWorkflowAdmin(admin.ModelAdmin):
    list_display = ["request_type", "initial_status"]
    search_fields = ["request_type", "initial_status"]
    list_filter = ["request_type"]
