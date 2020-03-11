#  Copyright (c) Code Written and Tested by Ahmed Emad in 11/03/2020, 12:21.

from django.urls import path

from core.views import user_login, user_logout, UserProfileView

app_name = 'core'

urlpatterns = [
    path('users/signup', UserProfileView.as_view({'post': 'create'}), name='signup'),
    path('users/login', user_login, name='login'),
    path('users/logout', user_logout, name='logout'),
    path('users/me', UserProfileView.as_view({'get': 'retrieve',
                                              'put': 'update',
                                              'patch': 'partial_update',
                                              'delete': 'destroy'}), name='user-details'),
    path('notebooks/'),
    path('notebooks/<int:notebook_sort>/notes'),
    path('notebooks/<int:notebook_sort>/notes/attachment')
]
