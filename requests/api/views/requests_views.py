from rest_framework.generics import CreateAPIView, UpdateAPIView
from requests.api.serializers import (
    CreateRequestSerializer,
    CreateRequestApprovalSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from requests.services.requests_commands import RequestCommands
from requests.models import Request


class CreateRequestView(CreateAPIView):
    serializer_class = CreateRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Request created successfully"}, status=status.HTTP_201_CREATED
        )


class UpdateRequestsForGFSAToReviewView(UpdateAPIView):

    def update(self, request, *args, **kwargs):
        updated_requests, warnings = (
            RequestCommands().update_requests_under_gfsa_review()
        )
        return Response(
            {
                "message": "Requests under GFSA review updated successfully",
                "updated_requests": updated_requests,
                "warnings": warnings,
            },
            status=status.HTTP_200_OK,
        )


class CreateRequestApprovalView(CreateAPIView):
    serializer_class = CreateRequestApprovalSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request: Request = serializer.save()
        return Response(
            {
                "message": f"Request {request.number} transition successfully to status: {request.status.name_en}"
            },
            status=status.HTTP_201_CREATED,
        )
