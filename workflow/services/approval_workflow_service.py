from requests.models import RequestType, RequestStatus
from workflow.models import ApprovelWorkflow
from rest_framework.exceptions import ValidationError
from typing import Dict, Any, Optional, List
from django.db.models import F
from workflow.models import Transition


class ApprovalWorkflowService:
    """
    Service for approval workflows related operations.
    """

    def get_initial_status(self, request_type: RequestType) -> RequestStatus:
        """
        Get the initial status for a request type.
        """
        workflow: ApprovelWorkflow = self.get_workflow({"request_type": request_type})
        if not workflow.initial_status:
            raise ValidationError(f"No initial status found for workflow: {workflow}")
        return workflow.initial_status

    def get_workflow(self, filters: Dict[str, Any]) -> ApprovelWorkflow:
        """
        Get a workflow by filters.
        """
        if not filters:
            raise ValidationError("Filters are required to get workflow")
        workflow = ApprovelWorkflow.objects.filter(**filters).first()
        if not workflow:
            raise ValidationError(f"No workflow found for filters: {filters}")
        return workflow

    def get_all_workflows(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get all workflows.
        """
        return self._get_detailed_transition()

    def get_workflow_for_request_type(
        self, request_type: str
    ) -> Dict[str, List[Dict[str, Any]]]:
        workflow_transitions = self._get_detailed_transition(
            filters={"workflow__request_type__code": request_type}
        )
        if not workflow_transitions:
            raise ValidationError(f"No workflow found for request type: {request_type}")
        return workflow_transitions

    def _get_detailed_transition(
        self, filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        rows = Transition.objects.filter(**(filters or {})).values(
            action_name_en=F("action__name_en"),
            from_status_name_en=F("from_status__name_en"),
            to_status_name_en=F("to_status__name_en"),
            initial_status_name_en=F("workflow__initial_status__name_en"),
            is_final_status=F("is_final"),
            request_type_name_en=F("workflow__request_type__name_en"),
        )

        workflows: Dict[str, List[Dict[str, Any]]] = {}
        for row in rows:
            request_type_name = row["request_type_name_en"]
            transition = {
                key: value
                for key, value in row.items()
                if key != "request_type_name_en"
            }
            workflows.setdefault(request_type_name, []).append(transition)
        workflows["count"] = len(rows)
        return workflows
