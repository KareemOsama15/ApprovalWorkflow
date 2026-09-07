from django.urls import path
from requests.api.views import (
    CreateRequestView,
    CreateRequestApprovalView,
    UpdateRequestsForGFSAToReviewView,
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
]
