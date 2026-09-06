from django.urls import path
from requests.api.views import (
    CreateRequestView,
    CreateRequestApprovalView,
    UpdateRequestsForGFSAToReviewView,
    GetRequestWorkflowView,
    GetAllWorkflowsView,
    CreateRequestTypeApprovalWorkflowView,
    CreateActionView,
    CreateWorkflowTransitionView,
    UpdateWorkflowTransitionView,
)

urlpatterns = [
    path("create", CreateRequestView.as_view(), name="create-request"),
    path(
        "update-gfsa-to-review-status",
        UpdateRequestsForGFSAToReviewView.as_view(),
        name="update-gfsa-to-review-status",
    ),
    path(
        "approval/create",
        CreateRequestApprovalView.as_view(),
        name="create-request-approval",
    ),
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
