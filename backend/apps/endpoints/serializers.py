from rest_framework import serializers
from apps.endpoints.models import Endpoint, MLAlgorithm, MLAlgorithmStatus, MLRequest


class EndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        fields = '__all__'
        read_only_fields = ('id', 'created_at')


class MLAlgorithmSerializer(serializers.ModelSerializer):
    current_status = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MLAlgorithm
        fields = ('id', 'name', 'description', 'code', 'version', 'owner', 'created_at', 'parent_endpoint', 'current_status')
        read_only_fields = ('id', 'created_at')

    def get_current_status(self, instance):
        """Get the current active status of the algorithm"""
        try:
            status = MLAlgorithmStatus.objects.filter(
                parent_mlalgorithm=instance,
                active=True
            ).latest('created_at')
            return status.status
        except MLAlgorithmStatus.DoesNotExist:
            return None


class MLAlgorithmStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLAlgorithmStatus
        fields = '__all__'
        read_only_fields = ('id', 'created_at')


class MLRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLRequest
        fields = '__all__'
        read_only_fields = ('id', 'created_at')
