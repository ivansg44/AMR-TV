from django.urls import include, path
from rest_framework import routers

from amr_tv.isolate.views import IsolateViewSet


router = routers.DefaultRouter()
router.register(r"isolates", IsolateViewSet)

urlpatterns = [
    path("", include(router.urls))
]
