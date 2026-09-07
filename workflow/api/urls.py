from django.urls import path
from workflow.api.views import (
    GetRequestWorkflowView,
    GetAllWorkflowsView,
    CreateRequestTypeApprovalWorkflowView,
    CreateActionView,
    CreateWorkflowTransitionView,
    UpdateWorkflowTransitionView,
)

urlpatterns = [
    path(
        "get-request-workflow",
        GetRequestWorkflowView.as_view(),
        name="get-request-workflow",
    ),
    path(
        "get-all-workflows",
        GetAllWorkflowsView.as_view(),
        name="get-all-workflows",
    ),
    path(
        "approval-workflow/create",
        CreateRequestTypeApprovalWorkflowView.as_view(),
        name="create-approval-workflow",
    ),
    path(
        "action/create",
        CreateActionView.as_view(),
        name="create-workflow-action",
    ),
    path(
        "workflow-transition/create",
        CreateWorkflowTransitionView.as_view(),
        name="create-workflow-transition",
    ),
    path(
        "workflow-transition/update/<int:transition_id>",
        UpdateWorkflowTransitionView.as_view(),
        name="update-workflow-transition",
    ),
]
