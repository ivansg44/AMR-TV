from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.views import defaults as default_views
from django.views.generic import TemplateView

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("isolates/", include("amr_tv.isolate.urls")),
    path("amr-genotypes/", include("amr_tv.amr_genotype.urls")),
    path("transmission-events/", include("amr_tv.transmission_events.urls")),
    path("adjacency-matrix/", include("amr_tv.adjacency_matrix.urls")),
    path("node-link-diagram/", include("amr_tv.node_link_diagram.urls")),
    path("node-detail-table/", include("amr_tv.node_detail_table.urls")),
    path("", TemplateView.as_view(template_name="base.html"))
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
