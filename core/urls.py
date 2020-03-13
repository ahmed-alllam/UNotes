#  Copyright (c) Code Written and Tested by Ahmed Emad in 13/03/2020, 20:02.

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.views import user_login, user_logout, UserProfileView, NoteBookView, NoteView, NoteAttachmentView

app_name = 'core'

note_book_router = DefaultRouter()
note_book_router.register('', NoteBookView, basename='notebooks')

note_router = DefaultRouter()
note_router.register('', NoteView, basename='notes')

note_attachment_router = DefaultRouter()
note_attachment_router.register('', NoteAttachmentView, basename='attachments')

urlpatterns = [
    path('users/signup/', UserProfileView.as_view({'post': 'create'}), name='signup'),
    path('users/login/', user_login, name='login'),
    path('users/logout/', user_logout, name='logout'),
    path('users/me/', UserProfileView.as_view({'get': 'retrieve',
                                               'put': 'update',
                                               'patch': 'partial_update',
                                               'delete': 'destroy'}), name='user-details'),
    path('notebooks/', include(note_book_router.urls)),
    path('notebooks/<slug:notebook_slug>/notes/', include(note_router.urls)),
    path('notebooks/<slug:notebook_slug>/notes/<slug:note_slug>/attachment/', include(note_attachment_router.urls))
]
