from django.urls import path
from amr_tv.node_detail_table.views import node_detail_table_view

urlpatterns = [
    path("", view=node_detail_table_view)
]
