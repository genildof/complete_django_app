import pandas as pd
from datetime import datetime
import pytz
from apps.pedidos.models import Pedido, ChangeLog

from django.dispatch import receiver

BR_TIMEZONE = pytz.timezone('America/Sao_Paulo')
DATE_FORMAT = '%Y-%m-%d %X'
ALTO_VALOR_PARAM = 1000.00
STRING_TYPE = 'string'
DATE_TYPE = 'date'
FLOAT_TYPE = 'float'
INTEGER_TYPE = 'integer'


def convert_excel_to_dataframe(uploaded_file_url, linha_cabecalho=0):
    # define cabeçalho na linha 3 - header 2
    excel_data = pd.read_excel("." + uploaded_file_url, header=linha_cabecalho)
    return pd.DataFrame(excel_data)


def upload_status_list(dataframe):

    updated_records = 0
    not_found = 0
    reviewed_records = 0

    for row in dataframe.itertuples(index=True):

        checked_pedido = get_cell_value(row, 'Pedido', STRING_TYPE, 14)
        checked_pendencia = get_cell_value(row, 'Pendencia', STRING_TYPE, 12)
        checked_previsao = get_cell_value(row, 'Previsao', DATE_TYPE)

        # Review if exists
        if Pedido.objects.filter(pedido=checked_pedido).exists():

            obj = Pedido.objects.get(pedido=checked_pedido)
            some_change = True
            compared = ''

            for value in Pedido.PendenciaMacro.values:

                if checked_pendencia in value.lower():
                    print(f'"{value.lower()}" contains "{checked_pendencia}"')
                else:
                    print(
                        f'"{value.lower()}" does not contain "{checked_pendencia}"')

            print(
                f"Pedido: {checked_pedido}\t\t\tPendencia: {checked_pendencia}\t\t\tPrevisao: {checked_previsao}")

            if some_change:
                updated_records += 1

            reviewed_records += 1

        # If not found
        else:

            try:

                not_found += 1

            except Exception as e:
                print(str(e) + "\nPedido: " + checked_pedido)

    return {'not_found': not_found, 'reviewed_records': reviewed_records, 'updated_records': updated_records}


def is_report_b2b_valid(dataframe):
    print('\nDataFrame keys:')
    print(dataframe.keys())
    print('\nDataframe key #146 label: ' +
          dataframe.columns.values[146] + ' | Expected: Soma de Delta_REC_LIQ')
    return False if (dataframe.columns.values[146] != 'Soma de Delta_REC_LIQ') else True


def upload_report_b2b(dataframe):

    updated_records = 0
    new_records = 0
    reviewed_records = 0

    # renames columns that contains spaces
    dataframe.columns.values[1] = 'ID_Vantive'
    dataframe.columns.values[146] = 'Delta_REC_LIQ'

    for row in dataframe.itertuples(index=True):

        checked_pedido = get_cell_value(row, 'Pedido', STRING_TYPE, 14)
        checked_id_vantive = get_cell_value(row, 'ID_Vantive', INTEGER_TYPE)
        checked_wcd = get_cell_value(row, 'Num_WCD', INTEGER_TYPE)
        checked_atp = get_cell_value(row, 'Num_ATP', STRING_TYPE, 7, 'ETP')
        checked_velocidade = get_cell_value(row, 'Velocidade', STRING_TYPE, 8)
        checked_wcd_tarefa = get_cell_value(
            row, 'WCD_Tarefa_Rede', STRING_TYPE, 30)
        checked_nova_quebra = get_cell_value(
            row, 'Nova_Quebra', STRING_TYPE, 17)
        checked_esteira = get_cell_value(row, 'Esteira', STRING_TYPE, 2)
        checked_classificacao = get_cell_value(
            row, 'Classificacao_Resumo_Atual', STRING_TYPE, 24)
        checked_delta_rec = get_cell_value(row, 'Delta_REC_LIQ', FLOAT_TYPE)
        checked_carteira = get_cell_value(row, 'Carteira', STRING_TYPE, 14)
        checked_data_entrada = get_cell_value(row, 'Data_Entrada', DATE_TYPE)
        checked_data_tecnica = get_cell_value(row, 'DataTecnica', DATE_TYPE)
        checked_data_rede = get_cell_value(row, 'DataRede', DATE_TYPE)
        checked_data_planejada = get_cell_value(
            row, 'Data_Planejada', DATE_TYPE)
        checked_servico = get_cell_value(row, 'Servico', STRING_TYPE, 22)
        checked_sla = get_cell_value(row, 'SLA', STRING_TYPE, 11)
        checked_segmento = get_cell_value(row, 'SegmentoNovo', STRING_TYPE, 12)
        checked_esteira_regionalizada = get_cell_value(
            row, 'Esteira_Regionalizada', STRING_TYPE, 22)
        checked_cliente = get_cell_value(row, 'Cliente', STRING_TYPE, 100)
        checked_cidade = get_cell_value(row, 'Cidade', STRING_TYPE, 30)
        checked_cadeia = get_cell_value(
            row, 'Cadeia_Pendencias_Descricao', STRING_TYPE, 30)

        # Review if exists
        if Pedido.objects.filter(pedido=checked_pedido).exists():

            obj = Pedido.objects.get(pedido=checked_pedido)
            some_change = False

            some_change = update_if_changes(
                obj, 'data_rede', obj.data_rede, checked_data_rede) if some_change == False else some_change
            some_change = update_if_changes(
                obj, 'data_planejada', obj.data_planejada, checked_data_planejada) if some_change == False else some_change
            some_change = update_if_changes(
                obj, 'data_tecnica', obj.data_tecnica, checked_data_tecnica) if some_change == False else some_change
            some_change = update_if_changes(
                obj, 'carteira', obj.carteira, checked_carteira) if some_change == False else some_change
            some_change = update_if_changes(
                obj, 'classificacao_resumo', obj.classificacao_resumo, checked_classificacao) if some_change == False else some_change

            if some_change:
                updated_records += 1

            reviewed_records += 1

        # If not existes creates new
        else:

            try:

                Pedido.objects.create(
                    pedido=checked_pedido, id_vantive=checked_id_vantive,
                    num_wcd=checked_wcd, num_atp=checked_atp, servico=checked_servico,
                    velocidade=checked_velocidade, sla=checked_sla,
                    carteira=checked_carteira, segmento=checked_segmento,
                    esteira_regionalizada=checked_esteira_regionalizada,
                    cliente=checked_cliente, cidade=checked_cidade,
                    cadeia_pendencias_descricao=checked_cadeia,
                    data_tecnica=checked_data_tecnica, wcd_tarefa_rede=checked_wcd_tarefa,
                    data_entrada=checked_data_entrada, data_planejada=checked_data_planejada,
                    data_rede=checked_data_rede,
                    delta_rec_total=checked_delta_rec, esteira=checked_esteira,
                    classificacao_resumo=checked_classificacao, nova_quebra=checked_nova_quebra
                )

                new_records += 1

            except Exception as e:
                print(str(e) + "\nPedido: " + checked_pedido)

    return {'new_records': new_records, 'reviewed_records': reviewed_records, 'updated_records': updated_records}


# Powered function for extracting excel cell's values
def get_cell_value(row, column, type=STRING_TYPE, string_lenght=None, remove=None):

    try:

        value = getattr(row, column, None)

        match type:

            case "string":
                value = str(value)
                if string_lenght:
                    value = value[:string_lenght]
                if remove:
                    value = value.replace(remove, "")

            case "date":
                value = format_date(value)

            case "integer":
                value = round(value)

            case "float":
                value = float(value)

        return value

    except:
        return None


# Prepares date cells values for MariaDB date columns
def format_date(value):
    formated_date = BR_TIMEZONE.localize(
        datetime.strptime(str(value), DATE_FORMAT))
    return formated_date if str(value) != "NaT" else None


# Creates a ChangLog for every field changes
def update_if_changes(obj, field_name, old, new):
    updated = False

    if (field_changed(new, old)):
        ChangeLog.objects.create(pedido=obj, field_name=field_name,
                                 old_value=old, new_value=new)
        setattr(obj, field_name, new)
        print(
            f'pedido: {obj.pedido} - field_name: {field_name} - old: {old} - new: {getattr(obj, field_name)}')
        obj.save(update_fields=[field_name])
        updated = True

    return updated


# Compare values
def field_changed(new, old):
    return True if (new != old) else False
