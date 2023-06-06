# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import Pedido, ChangeLog
from django import forms

# Register your models here.


@admin.register(ChangeLog)
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")


class PedidoAdminForm(forms.ModelForm):

    class Meta:
        model = Pedido
        fields = "__all__"


class PedidoAdmin(admin.ModelAdmin):
    form = PedidoAdminForm
    list_display = [
        "nova_quebra",
        "rede_contratada",
        "data_entrada",
        "servico",
        # "updated_at",
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
        # "created_at",
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
    readonly_fields = [
        "nova_quebra",
        "rede_contratada",
        "data_entrada",
        "servico",
        # "updated_at",
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
        # "created_at",
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


admin.site.register(Pedido, PedidoAdmin)
