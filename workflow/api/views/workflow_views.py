from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    ListAPIView,
    UpdateAPIView,
)
from rest_framework.response import Response
from rest_framework import status
from workflow.api.serializers import (
    CreateRequestTypeApprovalWorkflowSerializer,
    CreateActionSerializer,
)
from workflow.services.approval_workflow_service import ApprovalWorkflowService
from workflow.services.transition_service import TransitionService


class GetRequestWorkflowView(RetrieveAPIView):
    """
    Get a request workflow.
    """

    def retrieve(self, request, *args, **kwargs):
        request_type = request.query_params.get("request_type")
        if not request_type:
            return Response(
                {"message": "Request type is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        workflow = ApprovalWorkflowService().get_workflow_for_request_type(request_type)
        return Response(
            {"data": workflow},
            status=status.HTTP_200_OK,
        )


class GetAllWorkflowsView(ListAPIView):
    """
    Get all workflows.
    """

    def list(self, request, *args, **kwargs):
        workflows = ApprovalWorkflowService().get_all_workflows()
        return Response(
            {"data": workflows},
            status=status.HTTP_200_OK,
        )


class CreateRequestTypeApprovalWorkflowView(CreateAPIView):
    """
    Create a request type approval workflow.
    """

    serializer_class = CreateRequestTypeApprovalWorkflowSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"data": "Request type approval workflow created successfully"},
            status=status.HTTP_201_CREATED,
        )


class CreateActionView(CreateAPIView):
    """
    Create an action.
    """

    serializer_class = CreateActionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"data": "Action created successfully"},
            status=status.HTTP_201_CREATED,
        )


class CreateWorkflowTransitionView(CreateAPIView):
    """
    Create a workflow transition.
    """

    def create(self, request, *args, **kwargs):
        TransitionService().create_workflow_transition(request.data)
        return Response(
            {"data": "Workflow transition created successfully"},
            status=status.HTTP_201_CREATED,
        )


class UpdateWorkflowTransitionView(UpdateAPIView):
    """
    Update a workflow transition.
    """

    def update(self, request, *args, **kwargs):
        try:
            transition_id = kwargs.get("transition_id")
            TransitionService().update_workflow_transition(request.data, transition_id)
            return Response(
                {"data": "Workflow transition updated successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
