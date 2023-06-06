from rest_framework import viewsets, permissions

from . import serializers
from . import models


class PedidoViewSet(viewsets.ModelViewSet):
    """ViewSet for the Pedido class"""

    queryset = models.Pedido.objects.all()
    serializer_class = serializers.PedidoSerializer
    permission_classes = [permissions.IsAuthenticated]
