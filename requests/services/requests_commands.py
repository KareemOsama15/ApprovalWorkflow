from django.db.models import F, QuerySet
from django.db import transaction
from requests.models import Request
from typing import Any, Dict, Optional, List
from requests.services.workflow_services import WorkflowServices
from requests.models import RequestSequence, Transition, RequestProduct
import random


class RequestCommands:

    SEQUENCE_FORMAT = "REQ-{:06d}"

    def __init__(self):
        self.workflow_services = WorkflowServices()

    def create_request(self, data: Dict[str, Any]) -> Request:
        with transaction.atomic():
            products = data.pop("products", [])
            data["number"] = self._generate_request_number()
            data["status"] = self.workflow_services.get_initial_status(data["type"])
            request = Request.objects.create(**data)
            self.create_products(request, products)
            return request

    def create_request_approval(self, data: Dict[str, Any]) -> Request:
        workflow_services = WorkflowServices()
        request: Request = data["request"]
        transition: Transition = workflow_services.handle_request_transition(data)
        if transition:
            self._update_request_status(request, transition)

        return request

    def _generate_request_number(self) -> str:
        last_request: Optional[RequestSequence] = (
            RequestSequence.objects.select_for_update().order_by("-sequence").first()
        )
        if last_request:
            last_seq = last_request.sequence
            last_request.sequence = F("sequence") + 1
            last_request.save()
            return self.SEQUENCE_FORMAT.format(last_seq + 1)
        else:
            RequestSequence.objects.create(sequence=1)
            return self.SEQUENCE_FORMAT.format(1)

    def create_products(self, request: Request, products: List[Dict[str, Any]]) -> None:
        for product in products:
            RequestProduct.objects.create(
                request=request,
                product_id=product["code"],
                asked_quantity=product["asked_quantity"],
            )

    def get_requests(self, filters: Dict[str, Any]) -> QuerySet[Request]:
        return Request.objects.select_related("type", "status").filter(**filters)

    def update_requests_under_gfsa_review(self) -> None:
        requests = self.get_requests(filters={"status__code": 14})
        updated_requests = {}
        warnings = []
        for request in requests:
            action = "gfsa_action"
            status_id = random.choice([7, 9, 15])
            transition: Optional[Transition] = (
                self.workflow_services.handle_gfsa_request_status_update(
                    request=request, action=action, status_id=status_id
                )
            )
            if transition:
                self._update_request_status(request, transition)
                updated_requests[request.number] = status_id
            else:
                warnings.append(f"Request {request.number} not updated")
        return updated_requests, warnings

    def _update_request_status(self, request: Request, transition: Transition) -> None:
        if request.status == transition.to_status:
            return
        request.status = transition.to_status
        request.save(update_fields=["status"])
