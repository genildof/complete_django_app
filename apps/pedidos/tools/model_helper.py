from apps.pedidos.models import Pedido
import pandas as pd
from django.db.models import Q
from datetime import datetime, timedelta
from datetime import datetime
import pytz

CARTEIRAS_CENTRALIZADO = ['Viabilidade', 'Planejamento', 'TI']
CARTEIRAS_VISTORIA = ['Vistoria']
CARTEIRAS_ATIVACAO = ['Ativação', 'Implantacao']
CARTEIRAS_ENGENHARIA = ['Transporte', 'Engenharia']
CARTEIRAS_REDE = ['Rede']
CARTEIRAS_REGIONAL = CARTEIRAS_VISTORIA + CARTEIRAS_REDE + \
    CARTEIRAS_ATIVACAO + CARTEIRAS_ENGENHARIA
ESTEIRAS = ['PE']
STATUS_PENDENCIA = 'ATUALIZAR'
ORDER_BY = 'carteira'
SEGMENTO_FIELD = 'segmento'
FILTRO_PADRAO = ['Técnica']
DISCARD_ON_FILTERING = 'Todos'
DAYS_UPDATED = 3
BR_TIMEZONE = pytz.timezone('America/Sao_Paulo')
DATE_FORMAT = '%Y-%m-%d'


def get_global_statistics():

    # print (f"Pedidos sem data: {get_pedidos_datar_ativacao(CARTEIRAS_REGIONAL).count()}")

    pedidos_regional = get_pedidos_by_carteira(CARTEIRAS_REGIONAL).count()
    pedidos_atualizar = get_pedidos_atualizar_status().count()
    pedidos_atualizados = (pedidos_atualizar - pedidos_atualizar)

    return {
        'entrante_7_dias': [45, 50, 47, 33, 50, 22, 3],
        'atualizados_7_dias': [30, 50, 40, 37, 60, 90, 25],
        'datas_7_dias': get_chart_date_list(get_date_range_3(7)).tolist(),
        'days_updated': DAYS_UPDATED,
        'pedidos_tecnica': get_pedidos_tecnica().count(),
        'datar_rede': get_pedidos_datar_rede().count(),
        'datar_vistoria': get_pedidos_datar_ativacao(CARTEIRAS_VISTORIA).count(),
        'datar_ativacao_rede': get_pedidos_datar_ativacao(CARTEIRAS_REDE).count(),
        'datar_engenharia': get_pedidos_datar_ativacao(CARTEIRAS_ENGENHARIA).count(),
        'datar_ativacao': get_pedidos_datar_ativacao(CARTEIRAS_ATIVACAO).count(),
        'pedidos_centralizado': get_pedidos_by_carteira(CARTEIRAS_CENTRALIZADO).count(),
        'pedidos_vistoria': get_pedidos_by_carteira(CARTEIRAS_VISTORIA).count(),
        'pedidos_rede': get_pedidos_by_carteira(CARTEIRAS_REDE).count(),
        'pedidos_engenharia': get_pedidos_by_carteira(CARTEIRAS_ENGENHARIA).count(),
        'pedidos_ativacao': get_pedidos_by_carteira(CARTEIRAS_ATIVACAO).count(),
        'pedidos_regional': pedidos_regional,
        'pedidos_atualizar': pedidos_atualizar,
        'pedidos_atualizados': pedidos_atualizados,
    }


def get_segmento_statistics():
    # array com resumo dos pedidos em cada segmento e carteiras no backlog técnico

    statistics = []

    for row in get_segmento_list():

        segmento = row.get(SEGMENTO_FIELD)

        centralizado = Pedido.objects.filter(
            segmento=segmento, carteira__in=CARTEIRAS_CENTRALIZADO, esteira__in=ESTEIRAS).count()

        vistoria = Pedido.objects.filter(
            segmento=segmento, carteira__in=CARTEIRAS_VISTORIA,  esteira__in=ESTEIRAS).count()

        ativação = Pedido.objects.filter(
            segmento=segmento, carteira__in=CARTEIRAS_ATIVACAO,  esteira__in=ESTEIRAS).count()

        rede = Pedido.objects.filter(
            segmento=segmento, carteira__in=CARTEIRAS_REDE,  esteira__in=ESTEIRAS).count()

        desatualizados = Pedido.objects.filter(
            pendencia_macro=STATUS_PENDENCIA, carteira__in=CARTEIRAS_REGIONAL, esteira__in=ESTEIRAS).count()

        statistics.append([segmento, centralizado, vistoria, rede, ativação, round(
            desatualizados/(vistoria + rede + ativação), 1)])

    return statistics


def set_backlog_queryset_filter(pedido, segmento, pendencia, cliente):
    # returns queryset

    queryset = get_pedidos_by_carteira(
        CARTEIRAS_ATIVACAO)  # get_default_queryset()

    if pedido:
        queryset = queryset.filter(Q(pedido__icontains=pedido) |
                                   Q(num_atp__icontains=pedido))

    if (segmento and segmento != DISCARD_ON_FILTERING):
        queryset = queryset.filter(Q(segmento__icontains=segmento))

    if (pendencia and pendencia != DISCARD_ON_FILTERING):
        queryset = queryset.filter(Q(pendencia_macro__icontains=pendencia))

    if cliente:
        queryset = queryset.filter(Q(cliente__icontains=cliente))

    return queryset


def format_date(value):
    return BR_TIMEZONE.localize(
        datetime.strptime(str(value), DATE_FORMAT))


def get_today_date():
    return format_date(datetime.now().date())


def get_default_queryset():
    # returns queryset
    return None


def get_pedidos_datar_rede(carteira=CARTEIRAS_REDE):
    # returns queryset
    return Pedido.objects.filter(Q(carteira__in=carteira) & Q(esteira__in=ESTEIRAS) &
                                 (Q(data_rede__isnull=True) | Q(data_rede__lt=get_today_date())))


def get_pedidos_datar_ativacao(carteira):
    # returns queryset
    return Pedido.objects.filter(Q(carteira__in=carteira) & Q(esteira__in=ESTEIRAS) &
                                 (Q(data_tecnica__isnull=True) | Q(data_tecnica__lt=get_today_date())))


def get_pedidos_atualizar_status(carteira=CARTEIRAS_REGIONAL):
    # returns queryset - trocar o 'or' por | quando houver pedidos atualizados
    return Pedido.objects.filter(Q(carteira__in=carteira) & Q(esteira__in=ESTEIRAS) &
                                 (Q(status_update__isnull=True) or Q(status_update__lte=(get_today_date() - timedelta(days=DAYS_UPDATED))))).order_by('-status_update')


def get_pedidos_by_carteira(carteira):
    # returns queryset
    return Pedido.objects.filter(carteira__in=carteira, esteira__in=ESTEIRAS).order_by(ORDER_BY)


def get_pedidos_tecnica():
    # returns queryset
    return Pedido.objects.filter(classificacao_resumo__in=FILTRO_PADRAO, esteira__in=ESTEIRAS).order_by(ORDER_BY)


def get_segmento_list():
    # returns dictionaty -- [{'segmento': 'Atacado'}...]
    return Pedido.objects.order_by(SEGMENTO_FIELD).values(SEGMENTO_FIELD).distinct()


def get_pendencia_list():
    # returns list -- ['ACESSO', 'AGENDADO', 'AGENDAR', 'ATUALIZAR'...]
    return Pedido.PendenciaMacro.values


def get_date_range_3(k=7):

    start = (datetime.today() - timedelta(days=k))

    df = pd.DataFrame({'date': pd.date_range(
        start=start.isoformat(), periods=k)})

    return df


def get_chart_date_list(df_range):

    return df_range.date.dt.strftime('%d/%b')
