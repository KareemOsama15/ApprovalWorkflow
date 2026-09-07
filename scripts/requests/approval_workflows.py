from requests.models import RequestType, RequestStatus
from workflow.models import ApprovelWorkflow


class CreateRequestsTypesBasedWorkflows:
    WORKFLOWS = [
        {
            "request_type": "JOIN_REQUEST",
            "initial_status": 1,
        },
        {
            "request_type": "UPDATE_PRODUCT_REQUEST",
            "initial_status": 10,
        },
        {
            "request_type": "CUSTOMER_CHANGE_INFO",
            "initial_status": 10,
        },
        {
            "request_type": "INCREASE_PRODUCT_REQUEST",
            "initial_status": 10,
        },
    ]

    def execute(self):
        print("Creating requests types based workflows...")
        for workflow in self.WORKFLOWS:
            request_type = RequestType.objects.get(code=workflow["request_type"])

            if not request_type:
                print(f"Request type {workflow['request_type']} not found")
                continue

            initial_status = RequestStatus.objects.get(code=workflow["initial_status"])
            if not initial_status:
                print(f"Initial status {workflow['initial_status']} not found")
                continue

            _, created = ApprovelWorkflow.objects.get_or_create(
                request_type=request_type,
                initial_status=initial_status,
            )
            if created:
                print(
                    f"Approval workflow for request type {workflow['request_type']} and initial status {workflow['initial_status']} created successfully"
                )

        print("All requests types based workflows created successfully..")
