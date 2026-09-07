from django.db import models


class ApprovelWorkflow(models.Model):
    request_type = models.ForeignKey(
        "requests.RequestType",
        on_delete=models.CASCADE,
        related_name="approval_workflows",
    )
    initial_status = models.ForeignKey(
        "requests.RequestStatus", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["request_type", "initial_status"],
                name="unique_request_type_initial_status",
            )
        ]

    def __str__(self):
        return f"{self.request_type.name_en} - {self.initial_status.name_en}"


class Action(models.Model):
    type = models.CharField(max_length=60, unique=True)
    name_en = models.CharField(max_length=50)
    name_ar = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.type}"


class Transition(models.Model):
    workflow = models.ForeignKey(
        ApprovelWorkflow, on_delete=models.CASCADE, related_name="transitions"
    )
    # allowed_roles = models.ManyToManyField(
    #     "requests.Role", related_name="allowed_roles_for_action", blank=True
    # )
    from_status = models.ForeignKey(
        "requests.RequestStatus", on_delete=models.CASCADE, related_name="from_status"
    )
    to_status = models.ForeignKey(
        "requests.RequestStatus", on_delete=models.CASCADE, related_name="to_status"
    )
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    is_final = models.BooleanField(
        default=False,
        help_text="Helps to determine if the transition can be final stage of the workflow for the request type or not",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.workflow.request_type.name_en} - {self.from_status.name_en} -> {self.to_status.name_en}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["workflow", "from_status", "to_status", "action"],
                name="unique_workflow_from_status_to_status_action",
            )
        ]
