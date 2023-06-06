from django.urls import path, include
from rest_framework import routers

from . import api
from . import views
from . import htmx


router = routers.DefaultRouter()
router.register("Pedido", api.PedidoViewSet)
from apps.pedidos import views


urlpatterns = [

    path('upl_pedidos.html', views.PedidosUpload.as_view(),name='upl_pedidos'),
    path('upl_status.html', views.StatusUpload.as_view(),name='upl_status'),
    path('tbl_pedidos.html', views.PedidoBacklog.as_view(), name='all'),

    path("api/v1/", include(router.urls)),
    path("", views.PedidoIndex.as_view(), name="apps_Pedido_index"),
    path("list/", views.PedidoListView.as_view(), name="apps_Pedido_list"),
    path("create/", views.PedidoCreateView.as_view(), name="apps_Pedido_create"),
    path("detail/<int:pk>/", views.PedidoDetailView.as_view(), name="apps_Pedido_detail"),
    path("update/<int:pk>/", views.PedidoUpdateView.as_view(), name="apps_Pedido_update"),
    path("delete/<int:pk>/", views.PedidoDeleteView.as_view(), name="apps_Pedido_delete"),

    path("htmx/Pedido/", htmx.HTMXPedidoListView.as_view(), name="apps_Pedido_htmx_list"),
    path("htmx/Pedido/create/", htmx.HTMXPedidoCreateView.as_view(), name="apps_Pedido_htmx_create"),
    path("htmx/Pedido/delete/<int:pk>/", htmx.HTMXPedidoDeleteView.as_view(), name="apps_Pedido_htmx_delete"),

]

