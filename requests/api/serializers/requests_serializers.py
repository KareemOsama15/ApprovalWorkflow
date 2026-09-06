from rest_framework import serializers
from requests.models import Request
from requests.models.customer import Customer
from requests.services.requests_commands import RequestCommands
from requests.models.request import RequestType


class CreateRequestSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), required=False
    )
    type = serializers.CharField()
    products = serializers.ListField(child=serializers.DictField(), required=False)

    class Meta:
        model = Request
        fields = ["type", "customer", "products"]

    def validate(self, attrs):
        type = attrs.get("type")
        request_type = RequestType.objects.filter(code=type).first()
        if not request_type:
            raise serializers.ValidationError("Invalid request type")
        attrs["type"] = request_type
        return attrs

    def create(self, validated_data):
        request_commands = RequestCommands()
        return request_commands.create(validated_data)
