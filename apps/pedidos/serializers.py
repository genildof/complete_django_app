from rest_framework import serializers

from . import models


class PedidoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Pedido
        fields = [
            "nova_quebra",
            "rede_contratada",
            "data_entrada",
            "servico",
            "updated_at",
            "rede_data_contratada",
            "cliente",
            "num_wcd",
            "data_planejada",
            "cadeia_pendencias_descricao",
            "segmento",
            "sla",
            "num_atp",
            "data_tecnica",
            "rede_status_sco",
            "velocidade",
            "status_update",
            "created_at",
            "rede_id_sco",
            "cidade",
            "delta_rec_total",
            "id_vantive",
            "esteira",
            "classificacao_resumo",
            "pedido",
            "carteira",
            "escalonado",
            "rede_status",
        ]
