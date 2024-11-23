from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator


class OperationLog(models.Model):

    station = models.ForeignKey('storage.Station', on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Histórico")
        verbose_name_plural = _("Históricos")

    def __str__(self):
        date = self.created_at.strftime("%d/%m/%Y %H:%M:%S")
        return f'{self.station.name} - {self.action} - {date}'


class CollectionRequest(models.Model):
    
    class StatusChoices(models.IntegerChoices):
        OPEN = 1, 'Aberta'
        CONFIRMED = 2, 'Confirmada'
        CANCELLED = 0, 'Cancelada'
    
    station = models.ForeignKey('storage.Station', on_delete=models.CASCADE, related_name='collection_request')
    created_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(
        choices=StatusChoices.choices,
        default=StatusChoices.OPEN,
    )

    class Meta:
        verbose_name = _("Pedido de Coleta")
        verbose_name_plural = _("Pedidos de Coleta")

    def __str__(self):
        return f'Coleta: {self.id} - {self.station.name} - {self.get_status_display()}'

    def set_logs(self):
        if self.status == CollectionRequest.StatusChoices.CONFIRMED:
            OperationLog.objects.create(
                station=self.station,
                action=f'Coleta confirmada - status: {self.get_status_display()}'
            )
        if self.status == CollectionRequest.StatusChoices.CANCELLED:
            OperationLog.objects.create(
                station=self.station,
                action=f'Coleta cancelada - status: {self.get_status_display()}'
            )


class Station(models.Model):
    name = models.CharField(max_length=100)
    volume = models.FloatField(default=0)
    capacity = models.FloatField(
        default=100,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0),
        ]
    )
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Estação")
        verbose_name_plural = _("Estações")

    def __str__(self):
        return f'{self.name} - Capacidade: {self.capacity} - Volume atual: {self.volume}'

    def volume_rule(self):
        if self.volume >= (0.80 * self.capacity):
            CollectionRequest.objects.create(station=self)
            OperationLog.objects.create(
                station=self,
                action=f'Pedido de coleta gerado automaticamente - volume: {self.volume}'
            )
    
    def save(self, *args, **kwargs):
        try:
            id = self.id
            super().save(*args, **kwargs)
            if not id:
                OperationLog.objects.create(
                        station=self,
                        action=f'Estação {self.name} criada com capacidade: {self.capacity}'
                    )
        except Exception as e:
            print(f'Error saving station: {e}')

    def reset_volume(self):
        old_volume = self.volume
        self.volume = 0
        self.save()
        OperationLog.objects.create(
            station=self,
            action=f'Volume reiniciado de: {old_volume} para: {self.volume}'
        )