from rest_framework import serializers
from requests.models import ApprovelWorkflow, Action, RequestType


class CreateRequestTypeApprovalWorkflowSerializer(serializers.ModelSerializer):

    request_type = serializers.CharField()

    class Meta:
        model = ApprovelWorkflow
        fields = ["request_type", "initial_status"]

    def validate(self, attrs):
        request_type_code = attrs.get("request_type")
        request_type = RequestType.objects.filter(code=request_type_code).first()
        if not request_type:
            raise serializers.ValidationError("Request type not found")
        attrs["request_type"] = request_type
        return attrs


class CreateActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Action
        fields = ["type", "name_en", "name_ar"]
