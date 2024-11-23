from rest_framework import serializers
from storage.models import Station, CollectionRequest, OperationLog


class StationSerializer(serializers.ModelSerializer):

    last_updated = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S')
    collection_request = serializers.SerializerMethodField()


    class Meta:
        model = Station
        fields = ['id', 'name', 'volume', 'capacity', 'last_updated', 'collection_request']

    def validate(self, data):
        if data.get('volume') > self.instance.capacity:
            raise serializers.ValidationError(
                "O volume atual não pode exceder a capacidade total."
            )
        if data.get('volume', 0) < 0:
            raise serializers.ValidationError(
                "O volume não pode ser negativo."
            )
        return data

    def get_collection_request(self, obj):
        collection_request = obj.collection_request.filter(status=CollectionRequest.StatusChoices.OPEN).first()
        return CollectionRequestSerializer(collection_request).data


class CollectionRequestSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S')
    
    class Meta:
        model = CollectionRequest
        fields = '__all__'

    def validate(self, data):
        if self.instance:
            if self.instance.status != CollectionRequest.StatusChoices.OPEN:
                raise serializers.ValidationError(
                    "A coleta já foi confirmada ou cancelada e não pode ser alterada."
                )
        return data


class OperationLogSerializer(serializers.ModelSerializer):
    
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S')

    class Meta:
        model = OperationLog
        fields = '__all__'


