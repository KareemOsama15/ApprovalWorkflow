from requests.models import (
    RequestType,
    RequestStatus,
    ApprovelWorkflow,
    Action,
    Transition,
    Request,
)
from rest_framework.exceptions import ValidationError
from typing import Dict, Any, Optional, List
from django.db.models import QuerySet, F


class WorkflowServices:

    def get_initial_status(self, request_type: RequestType) -> RequestStatus:
        workflow: ApprovelWorkflow = self.get_workflow({"request_type": request_type})
        if not workflow.initial_status:
            raise ValidationError(f"No initial status found for workflow: {workflow}")
        return workflow.initial_status

    def handle_request_transition(self, data: Dict[str, Any]) -> Request:
        request: Request = data["request"]
        action: Action = self.get_action(data["action"])
        workflow: ApprovelWorkflow = self.get_workflow({"request_type": request.type})
        transition: Transition = self.get_transition(
            filters={
                "workflow": workflow,
                "action": action,
                "from_status": request.status,
            }
        )
        self._update_request_status(request, transition)
        return request

    def handle_gfsa_request_status_update(
        self, request: Request, action: str, status_id: int
    ) -> Request:
        transition: Transition = self.get_transition(
            filters={
                "workflow__request_type": request.type,
                "action__type": action,
                "from_status": request.status,
                "to_status__code": status_id,
            }
        )
        self._update_request_status(request, transition)
        return request

    def get_action(self, action: str) -> Action:
        action = Action.objects.filter(type=action).first()
        if not action:
            raise ValidationError(f"No action found for type: {action}")
        return action

    def get_workflow(self, filters: Dict[str, Any]) -> ApprovelWorkflow:
        if not filters:
            raise ValidationError("Filters are required to get workflow")
        workflow = ApprovelWorkflow.objects.filter(**filters).first()
        if not workflow:
            raise ValidationError(f"No workflow found for filters: {filters}")
        return workflow

    def get_transition(self, filters: Dict[str, Any]) -> Transition:
        matches_transitions: QuerySet[Transition] = list(
            Transition.objects.filter(**filters)[:2]
        )
        if not matches_transitions:
            raise ValidationError(f"No transition found for filters: {filters}")
        if len(matches_transitions) > 1:
            raise ValidationError(f"Multiple transitions found for filters: {filters}")
        return matches_transitions[0]

    def get_workflow_for_request_type(
        self, request_type: str
    ) -> Dict[str, List[Dict[str, Any]]]:
        workflow_transitions = self._get_detailed_transition(
            filters={"workflow__request_type__code": request_type}
        )
        if not workflow_transitions:
            raise ValidationError(f"No workflow found for request type: {request_type}")
        return workflow_transitions

    def get_all_workflows(self) -> Dict[str, List[Dict[str, Any]]]:
        return self._get_detailed_transition()

    def create_workflow_transition(self, data: Dict[str, Any]) -> Transition:
        request_type = data.pop("request_type", None)
        workflow = self.get_workflow({"request_type__code": request_type})
        action = self.get_action(data.pop("action", None))
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
        transition = self.get_transition({"id": transition_id})
        transition.action = self.get_action(data.get("action"))
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

    def _update_request_status(self, request: Request, transition: Transition) -> None:
        if request.status == transition.to_status:
            return
        request.status = transition.to_status
        request.save(update_fields=["status"])
