from django.test import TestCase

from django.test import TestCase
from storage.models import Station, OperationLog, CollectionRequest


class StationModelTests(TestCase):
    def setUp(self):
        self.station = Station.objects.create(name="Lixo Eletrônico", capacity=100, volume=50)

    def test_station_creation_logs(self):
        logs = OperationLog.objects.filter(station=self.station)
        self.assertEqual(logs.count(), 1)
        self.assertEqual(logs.first().action, "Estação Lixo Eletrônico criada com capacidade: 100")

    def test_volume_rule_triggers_collection_request(self):
        self.station.volume = 80
        self.station.save()
        self.station.volume_rule()

        collection_requests = CollectionRequest.objects.filter(station=self.station)
        logs = OperationLog.objects.filter(station=self.station)

        self.assertEqual(collection_requests.count(), 1)
        self.assertEqual(logs.count(), 2)  # Criação e pedido automático
        self.assertIn("Pedido de coleta gerado automaticamente", logs.last().action)

    def test_reset_volume_logs(self):
        self.station.volume = 50
        self.station.save()
        self.station.reset_volume()

        logs = OperationLog.objects.filter(station=self.station)
        self.assertEqual(logs.last().action, "Volume reiniciado de: 50 para: 0")
        self.assertEqual(self.station.volume, 0)


class CollectionRequestModelTests(TestCase):
    def setUp(self):
        self.station = Station.objects.create(name="Estação 2", capacity=100, volume=90)
        self.collection_request = CollectionRequest.objects.create(station=self.station)

    def test_collection_request_creation(self):
        self.assertEqual(self.collection_request.status, CollectionRequest.StatusChoices.OPEN)
        self.assertEqual(str(self.collection_request), f"Coleta: {self.collection_request.id} - Estação 2 - Aberta")

    def test_set_logs_on_confirmed_status(self):
        self.collection_request.status = CollectionRequest.StatusChoices.CONFIRMED
        self.collection_request.set_logs()

        logs = OperationLog.objects.filter(station=self.station)
        self.assertEqual(logs.count(), 2)
        self.assertIn("Coleta confirmada", logs.last().action)

    def test_set_logs_on_cancelled_status(self):
        self.collection_request.status = CollectionRequest.StatusChoices.CANCELLED
        self.collection_request.set_logs()

        logs = OperationLog.objects.filter(station=self.station)
        self.assertEqual(logs.count(), 2)
        self.assertIn("Coleta cancelada", logs.last().action)


class OperationLogModelTests(TestCase):
    def setUp(self):
        self.station = Station.objects.create(name="Estação 3", capacity=100, volume=30)

    def test_operation_log_str(self):
        log = OperationLog.objects.create(station=self.station, action="Teste de log")
        self.assertIn("Teste de log", str(log))
