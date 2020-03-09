#  Copyright (c) Code Written and Tested by Ahmed Emad in 09/03/2020, 23:56.

from django.urls import path

app_name = 'core'

urlpatterns = [
    path('users/signup'),
    path('users/login'),
    path('users/logout'),
    path('users/<username>'),
    path('notebooks/'),
    path('notebooks/<int:notebook_sort>/notes'),
]
