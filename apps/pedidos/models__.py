# -*- encoding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

# Create your models here.


class Pedido(models.Model):

    pedido = models.CharField('Pedido', max_length=14)
    id_vantive = models.CharField('ID Vantive', max_length=7, null=True)
    num_wcd = models.CharField('WCD/SPE', max_length=7, null=True)
    num_atp = models.CharField('ATP', max_length=7, null=True)
    servico = models.CharField('Serviço', max_length=22, null=True)
    velocidade = models.CharField('Velocidade', max_length=8, null=True)
    sla = models.CharField('SLA', max_length=11, null=True)
    carteira = models.CharField('Carteira', max_length=14, null=True)
    segmento = models.CharField('Segmento', max_length=12, null=True)
    esteira = models.CharField('Esteira', max_length=2, null=True)
    nova_quebra = models.CharField('Nova Quebra', max_length=17, null=True)
    classificacao_resumo = models.CharField(
        'Classificação Resumo', max_length=24, null=True)
    esteira_regionalizada = models.CharField(
        'Esteira Regionalizada', max_length=22, null=True)
    cliente = models.CharField('Cliente', max_length=100, null=True)
    cidade = models.CharField('Cidade', max_length=30, null=True)
    delta_rec_total = models.DecimalField('Delta Receita',
                                          null=True, max_digits=8, decimal_places=2)

    cadeia_pendencias_descricao = models.CharField(
        'Cadeira Descrição', max_length=50, null=True)
    wcd_tarefa_rede = models.CharField(
        'WCD Tarefa Rede', max_length=30, null=True)

    data_entrada = models.DateTimeField('Data Entrada', null=True, blank=True)
    data_tecnica = models.DateTimeField('Data Tecnica', null=True, blank=True)
    data_planejada = models.DateTimeField(
        'Data Planejada', null=True, blank=True)
    data_rede = models.DateTimeField('Data Rede', null=True, blank=True)
    status_update = models.DateTimeField(
        'Status Update', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    rede_status = models.CharField(max_length=25, null=True)
    rede_id_sco = models.CharField(max_length=6, null=True)
    rede_status_sco = models.CharField(max_length=25, null=True)
    rede_contratada = models.CharField(max_length=25, null=True)
    rede_data_contratada = models.DateTimeField(
        'Data Contratada', null=True, blank=True)

    escalonado = models.BooleanField(default=False, null=True)

    class Estimativa(models.TextChoices):
        MES_CORRENTE = 'MES_CORRENTE', _('Mes Corrente')
        MES_FUTURO = 'MES_FUTURO', _('Mes Futuro')

    estimativa = models.CharField(
        'Pedido',
        max_length=12,
        choices=Estimativa.choices,
        default=Estimativa.MES_FUTURO,
    )

    class PendenciaMacro(models.TextChoices):
        ACESSO = 'ACESSO', _('Acesso Central')
        AGENDADO = 'AGENDADO', _('Agendado')
        AGENDAR = 'AGENDAR', _('Agendar')
        ATUALIZAR = 'ATUALIZAR', _('Atualizar o Status')
        CABO_INTERNO = 'CABO_INTERNO', _('Lancamento Interno')
        CADASTRO = 'CADASTRO', _('Cadastro Fenix')
        CAPACITACAO = 'CAPACITACAO', _('Capacitacao')
        PLATAFORMA = 'PLAT_ELEV', _('Prataforma Elevatória')
        DOCUMENTACAO = 'DOCUMENTACAO', _('Documentacao')
        DESPACHO = 'DESPACHO', _('Despacho')
        DWDM = 'DWDM', _('DWDM')
        EQUIPAMENTO = 'EQUIPAMENTO', _('Equipamento')
        ENTREGUE = 'ENTREGUE', _('Entregue')
        FIBRA_ABERTA = 'FIBRA_ABERTA', _('Fibra Aberta')
        FORNECEDOR = 'FORNECEDOR', _('Fornecedor')
        INFRA = 'INFRA', _('Infra Cliente')
        LINK_BAIXA = 'LINK_BAIXA', _('Link Baixa - DDR/SIP')
        PCC = 'PCC', _('Enviado Para PCC')
        PCC_CONFIRMAR = 'PCC_CONF', _('Validar envio PCC')
        RETORNO_PCC = 'RET_PCC', _('Validar retorno PCC')
        PLANEJAMENTO = 'PLANEJAMENTO', _('Planejamento')
        RETORNO_PLANEJAMENTO = 'RET_PLAN', _('Validar retorno Planejamento')
        PONTA_REMOTA = 'PONTA_REMOTA', _('Ponta Remota')
        RADIO_ACESSO = 'RADIO_ACESSO', _('Rádio Acesso')
        REDE_EXTERNA = 'REDE_EXTERNA', _('Rede Externa')
        REDE_DCN = 'REDE_DCN', _('Rede DCN')
        REFERENCIA = 'REFERENCIA', _('ATP Referencia')
        SEM_ATP = 'SEM_ATP', _('Sem ATP / WCD')
        TESTE_STRESS = 'TESTE_STRESS', _('Teste de Stress')
        TRANSPORTE = 'TRANSPORTE', _('Transporte')
        TRIAGEM = 'TRIAGEM', _('Triagem Revisar')
        VIABILIDADE = 'VIABILIDADE', _('Viabilidade')
        VISTORIA = 'VISTORIA', _('Vistoria')
        TESTE_OTDR = 'TESTE_OTDR', _('Teste OTDR')
        UPLINK = 'UPLINK', _('Uplink ERB Saturado')

    pendencia_macro = models.CharField(
        'Pendência Macro',
        max_length=12,
        choices=PendenciaMacro.choices,
        default=PendenciaMacro.ATUALIZAR,
    )

    def __str__(self):
        return self.pedido

    class Meta:
        ordering = ["-carteira"]

    @property
    def is_altovalor(self):
        "Returns how many days passed after last update"
        return self.delta_rec_total >= 1000.00


class Comentario(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    nota = models.CharField(max_length=200)

    def __str__(self):
        return self.nota


class ChangeLog(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=30)
    old_value = models.CharField(max_length=30, null=True)
    new_value = models.CharField(max_length=30, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f'{self.pedido} - {self.field_name} - {self.created_at}'


class TimeSeries(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class FibraAberta(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)

    class ReparoStatus(models.TextChoices):
        PENDENTE = 'PENDENTE', _('Pendente')
        REPARO_OK = 'REPARO_OK', _('Reparo OK')

    status = models.CharField(
        max_length=9,
        choices=ReparoStatus.choices,
        default=ReparoStatus.PENDENTE,
    )

    nota = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.pedido} - {self.status}'
