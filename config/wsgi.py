import os
import sys

from django.core.wsgi import get_wsgi_application

# This allows easy placement of apps within the interior
# amr_tv directory.
app_path = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
)
sys.path.append(os.path.join(app_path, "amr_tv"))

application = get_wsgi_application()
