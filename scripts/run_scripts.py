"""
Runs From Shell:
python manage.py shell

Then run the script:
from scripts.run_scripts import RunScripts
RunScripts().run()
"""

from scripts.requests.customer_category import CreateCustomerCategory
from scripts.requests.request_types import CreateRequestTypes
from scripts.requests.approval_workflows import CreateRequestsTypesBasedWorkflows
from scripts.requests.approval_actions import CreateApprovalActions
from scripts.requests.request_statuses import CreateRequestStatuses
from scripts.requests.product import CreateProducts
from django.db import transaction


class RunScripts:

    SCRIPTS = {
        "request_types": CreateRequestTypes,
        "request_statuses": CreateRequestStatuses,
        "products": CreateProducts,
        "customer_category": CreateCustomerCategory,
        "approval_actions": CreateApprovalActions,
        "approval_workflows": CreateRequestsTypesBasedWorkflows,
    }

    def __init__(self, scripts: list[str] = []) -> None:
        self.scripts = scripts

    @transaction.atomic
    def run(self):
        if not self.scripts:
            self.scripts = list(self.SCRIPTS.keys())

        for script in self.scripts:
            if script not in self.SCRIPTS:
                print(f"Script {script} not found")
                continue
            self.SCRIPTS[script]().execute()
