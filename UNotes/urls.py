#  Copyright (c) Code Written and Tested by Ahmed Emad in 09/03/2020, 23:56.

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls'))
]
