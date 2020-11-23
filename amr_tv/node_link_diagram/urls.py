from django.urls import path
from amr_tv.node_link_diagram.views import node_link_diagram_view

urlpatterns = [
    path("", view=node_link_diagram_view)
]
