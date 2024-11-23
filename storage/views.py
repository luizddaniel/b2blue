from rest_framework.response import Response
from rest_framework import status, views, viewsets
from storage.models import CollectionRequest, OperationLog, Station
from storage.serializers import CollectionRequestSerializer, OperationLogSerializer, StationSerializer


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        old_volume = instance.volume
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        OperationLog.objects.create(
            station=instance,
            action=f'Volume atualizado de: {old_volume} para: {instance.volume}'
        )
        instance.volume_rule()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CollectionRequestViewSet(viewsets.ModelViewSet):
    queryset = CollectionRequest.objects.select_related('station').all()
    serializer_class = CollectionRequestSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        instance.set_logs()
        if instance.status == CollectionRequest.StatusChoices.CONFIRMED:
            instance.station.reset_volume()
        return Response(serializer.data, status=status.HTTP_200_OK)


class HistoricoAPIView(views.APIView):

    def get(self, request, station_id):
        logs = OperationLog.objects.select_related('station').filter(station_id=station_id)
        serializer = OperationLogSerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
