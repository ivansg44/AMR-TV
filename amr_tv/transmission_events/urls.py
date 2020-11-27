from django.urls import path
from amr_tv.transmission_events.views import transmission_events_view

urlpatterns = [
    path("", view=transmission_events_view)
]
