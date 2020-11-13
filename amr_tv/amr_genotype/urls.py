from django.urls import include, path
from rest_framework import routers

from amr_tv.amr_genotype.views import AMRGenotypeViewSet


router = routers.DefaultRouter()
router.register(r"", AMRGenotypeViewSet)

urlpatterns = [
    path("", include(router.urls))
]
