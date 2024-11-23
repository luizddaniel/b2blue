from django.contrib import admin

from storage.models import Station, OperationLog, CollectionRequest

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'volume', 'capacity', 'last_updated')
    search_fields = ('id', 'name')


@admin.register(OperationLog)
class OperationLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'station', 'action', 'created_at')
    search_fields = ('station__name',)


@admin.register(CollectionRequest)
class CollectionRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'station', 'status', 'created_at')
    search_fields = ('station__name',)
