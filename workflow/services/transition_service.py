from typing import Dict, Any, Optional
from workflow.models import Transition
from rest_framework.exceptions import ValidationError
from workflow.services.action_service import ActionService
from workflow.services.approval_workflow_service import ApprovalWorkflowService
from django.db.models import QuerySet


class TransitionService:
    """
    Service for transitions related operations.
    """

    def __init__(self):
        self.action_service = ActionService()
        self.approval_workflow_service = ApprovalWorkflowService()

    def get_transition(self, filters: Dict[str, Any]) -> Optional[Transition]:
        """
        Get a transition by filters.
        """
        if not filters:
            raise ValidationError("Filters are required to get transition")

        matches_transitions: QuerySet[Transition] = list(
            Transition.objects.filter(**filters)[:2]
        )
        if not matches_transitions:
            raise ValidationError(f"No transition found for filters: {filters}")
        if len(matches_transitions) > 1:
            raise ValidationError(f"Multiple transitions found for filters: {filters}")
        return matches_transitions[0]

    def create_workflow_transition(self, data: Dict[str, Any]) -> Transition:
        """
        Create a workflow transition.
        """
        request_type = data.pop("request_type", None)
        workflow = self.approval_workflow_service.get_workflow(
            {"request_type__code": request_type}
        )
        action = self.action_service.get_action(data.pop("action", None))
        transition = Transition.objects.create(
            workflow=workflow,
            from_status_id=data.get("from_status"),
            to_status_id=data.get("to_status"),
            action=action,
            is_final=data.get("is_final"),
        )
        return transition

    def update_workflow_transition(
        self, data: Dict[str, Any], transition_id: int
    ) -> Transition:
        """
        Update a workflow transition.
        """
        transition = self.get_transition({"id": transition_id})
        transition.action = self.action_service.get_action(data.get("action"))
        transition.from_status_id = data.get("from_status")
        transition.to_status_id = data.get("to_status")
        transition.is_final = data.get("is_final")
        transition.save(
            update_fields=[
                "action",
                "from_status",
                "to_status",
                "is_final",
            ]
        )
        return transition
