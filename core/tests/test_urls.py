#  Copyright (c) Code Written and Tested by Ahmed Emad in 13/03/2020, 20:02.

from django.test import TestCase
from django.urls import reverse, resolve

from core.views import UserProfileView, user_login, user_logout, NoteBookView, NoteView, NoteAttachmentView


class TestUsers(TestCase):
    """Test for the users urls"""

    def test_signup(self):
        """test for signup url"""
        url = reverse('core:signup')
        self.assertEqual(resolve(url).func.__name__,
                         UserProfileView.as_view({'post': 'create'}).__name__)

    def test_login(self):
        """test for login url"""
        url = reverse('core:login')
        self.assertEqual(resolve(url).func, user_login)

    def test_logout(self):
        """test for logout url"""
        url = reverse('core:logout')
        self.assertEqual(resolve(url).func, user_logout)

    def test_user_details(self):
        """test for user details url"""
        url = reverse('core:user-details')
        self.assertEqual(resolve(url).func.__name__,
                         UserProfileView.as_view({'get': 'retrieve'}).__name__)


class TestNoteBook(TestCase):
    """Test for the notebook urls"""

    def test_notebook_create(self):
        """test for users notebook create url"""
        url = reverse('core:notebooks-list')
        self.assertEqual(resolve(url).func.__name__,
                         NoteBookView.as_view({'post': 'create'}).__name__)

    def test_notebook_detail(self):
        """test for users notebook details url"""
        url = reverse('core:notebooks-detail', kwargs={'slug': 'slug'})
        self.assertEqual(resolve(url).func.__name__,
                         NoteBookView.as_view({'get': 'retrieve'}).__name__)


class TestNote(TestCase):
    """Test for the note urls"""

    def test_note_create(self):
        """test for users note create url"""
        url = reverse('core:notes-list', kwargs={'notebook_slug': 'slug'})
        self.assertEqual(resolve(url).func.__name__,
                         NoteView.as_view({'post': 'create'}).__name__)

    def test_note_detail(self):
        """test for users note details url"""
        url = reverse('core:notes-detail', kwargs={'notebook_slug': 'slug', 'slug': 'slug'})
        self.assertEqual(resolve(url).func.__name__,
                         NoteView.as_view({'get': 'retrieve'}).__name__)


class TestNoteAttachments(TestCase):
    """Test for the users note attachments urls"""

    def test_attachments_list(self):
        """test for users attachments list url"""
        url = reverse('core:attachments-list', kwargs={'notebook_slug': 'slug', 'note_slug': 'slug'})
        self.assertEqual(resolve(url).func.__name__,
                         NoteAttachmentView.as_view({'get': 'list'}).__name__)

    def test_attachment_detail(self):
        """test for users attachments details url"""
        url = reverse('core:attachments-detail', kwargs={'notebook_slug': 'slug',
                                                         'note_slug': 'slug', 'slug': 'slug'})
        self.assertEqual(resolve(url).func.__name__,
                         NoteAttachmentView.as_view({'get': 'retrieve'}).__name__)
