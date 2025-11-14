"""
WebSocket consumers para atualizações em tempo real.
"""

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import DadosSensor, Motor, Sensor


class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'dashboard_updates'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json['type']
        
        if message_type == 'get_kpis':
            kpis = await self.get_kpis()
            await self.send(text_data=json.dumps({
                'type': 'kpis_update',
                'data': kpis
            }))

    # Receive message from room group
    async def sensor_update(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'sensor_data',
            'data': event['data']
        }))

    async def alert_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'alert',
            'data': event['data']
        }))

    @database_sync_to_async
    def get_kpis(self):
        return {
            'total_motores': Motor.objects.filter(ativo=True).count(),
            'total_sensores': Sensor.objects.filter(ativo=True).count(),
            'dados_hoje': DadosSensor.objects.filter(
                data_hora__date__gte=timezone.now().date()
            ).count(),
            'ultimos_dados': list(
                DadosSensor.objects.select_related('motor', 'sensor')
                .order_by('-data_hora')[:5]
                .values(
                    'motor__nome', 'sensor__tipo', 'valor', 
                    'temperatura', 'rpm', 'data_hora'
                )
            )
        }