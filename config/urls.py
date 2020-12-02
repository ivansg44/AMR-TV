from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("isolates/", include("amr_tv.isolate.urls")),
    path("transmission-events/", include("amr_tv.transmission_events.urls")),
    path("adjacency-matrix/", include("amr_tv.adjacency_matrix.urls")),
    path("node-link-diagram/", include("amr_tv.node_link_diagram.urls")),
    path("node-detail-table/", include("amr_tv.node_detail_table.urls")),
    path("", TemplateView.as_view(template_name="base.html"))
]
