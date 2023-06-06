# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include, re_path  # add this
from . import views

urlpatterns = [
    path('backlog/admin/', admin.site.urls),          # Django admin route
    path("backlog/", include("apps.authentication.urls")), # Auth routes - login / register

    # ADD NEW Routes HERE

    path("backlog/pedidos/", include("apps.pedidos.urls")),
    path('backlog/htmx/', views.htmx_home, name='htmx'),

    # Leave `Home.Urls` as last the last line
    #(here the 'fieldmanger' context word must be the sema as NGINX virtual server name)
    path("backlog/", include("apps.home.urls"))
]
