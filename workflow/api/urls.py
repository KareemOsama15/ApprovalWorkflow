from django.urls import path
from workflow.api.views import (
    GetWorkflowView,
    GetAllWorkflowsView,
    CreateActionView,
    CreateWorkflowTransitionView,
    UpdateWorkflowTransitionView,
    CreateApprovalWorkflowView,
)

urlpatterns = [
    path(
        "get",
        GetWorkflowView.as_view(),
        name="get-workflow",
    ),
    path(
        "list-all",
        GetAllWorkflowsView.as_view(),
        name="get-all-workflows",
    ),
    path(
        "approval-create",
        CreateApprovalWorkflowView.as_view(),
        name="create-approval-workflow",
    ),
    path(
        "action/create",
        CreateActionView.as_view(),
        name="create-workflow-action",
    ),
    path(
        "transition/create",
        CreateWorkflowTransitionView.as_view(),
        name="create-workflow-transition",
    ),
    path(
        "transition/update/<int:transition_id>",
        UpdateWorkflowTransitionView.as_view(),
        name="update-workflow-transition",
    ),
]
