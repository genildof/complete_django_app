# -*- encoding: utf-8 -*-

from django.views import generic
from . import forms
from . import models
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from apps.pedidos.tools import excel_wrapper, model_helper
from .models import Pedido
import os


class PedidoBaseView(View):
    model = Pedido
    queryset = model_helper.get_default_queryset()
    context_object_name = 'object_list'
    fields = '__all__'
    success_url = reverse_lazy('pedidos:all')

# @login_required(login_url="/login/")


class PedidoBacklog(PedidoBaseView, ListView):
    template_name = 'pedidos/tbl_pedidos.html'

    def get_context_data(self, **kwargs):
        context = super(PedidoBacklog, self).get_context_data(**kwargs)

        context['session_username'] = self.request.user.get_username()

        pedido = self.request.GET.get('pedido')  # self.kwargs['pedido']
        segmento = self.request.GET.get('segmento')
        pendencia = self.request.GET.get('pendencia')
        cliente = self.request.GET.get('cliente')

        queryset = model_helper.set_backlog_queryset_filter(
            pedido, segmento, pendencia, cliente)

        context['object_list'] = queryset
        if queryset:
            context['object_list_size'] = queryset.count()
        context['segmento_list'] = model_helper.get_segmento_list()
        context['pendencia_list'] = model_helper.get_pendencia_list()

        return context


class PedidoIndex(generic.ListView):
    template_name = 'pedidos/pedido_index.html'
    success_url = reverse_lazy('pedidos:all')

    model = models.Pedido
    # form_class = forms.PedidoForm


class PedidoListView(generic.ListView):
    model = models.Pedido
    form_class = forms.PedidoForm


class PedidoCreateView(generic.CreateView):
    model = models.Pedido
    form_class = forms.PedidoForm


class PedidoDetailView(generic.DetailView):
    model = models.Pedido
    form_class = forms.PedidoForm


class PedidoUpdateView(generic.UpdateView):
    model = models.Pedido
    form_class = forms.PedidoForm
    pk_url_kwarg = "pk"


class PedidoDeleteView(generic.DeleteView):
    model = models.Pedido
    success_url = reverse_lazy("apps_Pedido_list")


class PedidosUpload(View):
    success_url = reverse_lazy('pedidos:all')
    template_name = 'pedidos/upl_pedidos.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):

        fs = FileSystemStorage()
        request = self.request

        uploaded_file = request.FILES['myfile']

        print('\nUploading file ' + uploaded_file.name.upper())
        filename = fs.save(uploaded_file.name, uploaded_file)
        uploaded_file_url = fs.url(filename)

        # Begins data manipulation
        print('\nLoading data from ' + filename.upper())
        df = excel_wrapper.convert_excel_to_dataframe(uploaded_file_url, 2)

        print('DataFrame size (rows):', len(df))

        if excel_wrapper.is_report_b2b_valid(df):
            print('\nWorking, please wait...')
            statistcs = excel_wrapper.upload_report_b2b(df)
            print(statistcs)
        else:
            print("\nInvalid columns structure on file " + filename.upper())

        if os.path.isfile(filename):
            os.remove(filename)
            print('\n' + filename.upper() + ' was removed.\n')

        return render(request, self.template_name, {'total_pedidos': Pedido.objects.count()})


class StatusUpload(View):
    success_url = reverse_lazy('pedidos:all')
    template_name = 'pedidos/upl_status.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):

        fs = FileSystemStorage()
        request = self.request

        uploaded_file = request.FILES['myfile']

        print('\nUploading file ' + uploaded_file.name.upper())
        filename = fs.save(uploaded_file.name, uploaded_file)
        uploaded_file_url = fs.url(filename)

        """ Begins data manipulation """

        print('\nLoading data from ' + filename.upper())
        df = excel_wrapper.convert_excel_to_dataframe(uploaded_file_url, 0)

        print('DataFrame size (rows):', len(df))
        print('Working, plaase wait...')

        statistcs = excel_wrapper.upload_status_list(df)
        print(statistcs)

        if os.path.isfile(filename):
            os.remove(filename)
            print(filename.upper() + ' was removed.\n')

        return render(request, self.template_name, {'total_pedidos': Pedido.objects.count()})
