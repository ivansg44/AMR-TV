from django.urls import path
from amr_tv.adjacency_matrix.views import (adjacency_matrix_view,
                                           highlighted_adjacency_matrix_view)

urlpatterns = [
    path("", view=adjacency_matrix_view),
    path("highlighted/", view=highlighted_adjacency_matrix_view)
]
