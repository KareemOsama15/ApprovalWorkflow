from rest_framework.generics import CreateAPIView, UpdateAPIView
from requests.api.serializers import CreateRequestSerializer
from rest_framework.response import Response
from rest_framework import status
from requests.services.requests_commands import RequestCommands


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
        updated_requests = RequestCommands().update_requests_under_gfsa_review()
        return Response(
            {
                "message": "Requests under GFSA review updated successfully",
                "updated_requests": updated_requests,
            },
            status=status.HTTP_200_OK,
        )
