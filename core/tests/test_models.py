#  Copyright (c) Code Written and Tested by Ahmed Emad in 13/03/2020, 20:02.

import os

from django.contrib.auth.models import User
from django.test import TestCase

from core.models import NoteBookModel, NoteModel, NoteAttachmentModel, UserProfileModel, users_upload, \
    attachment_upload


class TestUsers(TestCase):
    """UnitTest for users models"""

    def test_upload_name_unique(self):
        """test for image and file upload unique id generator"""

        image_1_id = users_upload(None, 'image1')
        image_2_id = users_upload(None, 'image2')
        self.assertNotEquals(image_1_id, image_2_id)

        file_1_id = attachment_upload(None, 'file1')
        file_2_id = attachment_upload(None, 'file2')
        self.assertNotEquals(file_1_id, file_2_id)

    def test_user_str(self):
        """test for user __str__ unction"""

        user = User.objects.create_user(username='username', password='password')
        user_profile = UserProfileModel.objects.create(account=user)
        self.assertEqual(user_profile.__str__(), user.username)

    def test_user_account_delete(self):
        """test for account delete after profile deletion from signals"""

        account = User.objects.create_user(username='username', password='password')
        user_profile = UserProfileModel.objects.create(account=account)
        user_profile.delete()
        self.assertEqual(User.objects.filter(username='username').exists(), False)


class TestNoteBook(TestCase):
    """UnitTest for notebook model"""

    def test_notebook_slug_unique(self):
        """test for notebook slug uniqueness"""

        user = User.objects.create_user(username='username', password='password')
        user_profile = UserProfileModel.objects.create(account=user)

        notebook1 = NoteBookModel.objects.create(user=user_profile, title='notebook')
        self.assertEqual(notebook1.slug, 'notebook')

        notebook2 = NoteBookModel.objects.create(user=user_profile, title='notebook')
        self.assertEqual(notebook2.slug, 'notebook-2')
        self.assertNotEquals(notebook1.slug, notebook2.slug)

    def test_notebook_str(self):
        """test for notebook __str__ function"""

        user = User.objects.create_user(username='username', password='password')
        user_profile = UserProfileModel.objects.create(account=user)
        notebook = NoteBookModel.objects.create(user=user_profile, title='notebook')
        self.assertEqual(notebook.__str__(), notebook.title)


class TestNote(TestCase):
    """UnitTest for note model"""

    def test_note_slug_unique(self):
        """test for note slug uniqueness"""

        user = User.objects.create_user(username='username', password='password')
        user_profile = UserProfileModel.objects.create(account=user)

        notebook1 = NoteBookModel.objects.create(user=user_profile, title='notebook1')

        note1 = NoteModel.objects.create(notebook=notebook1, title='note')
        self.assertEqual(note1.slug, 'note')

        note2 = NoteModel.objects.create(notebook=notebook1, title='note')
        self.assertEqual(note2.slug, 'note-2')
        self.assertNotEquals(note1.slug, note2.slug)

        notebook2 = NoteBookModel.objects.create(user=user_profile, title='notebook2')
        note3 = NoteModel.objects.create(notebook=notebook2, title='note')
        self.assertEqual(note3.slug, 'note')

    def test_note_str(self):
        """test for note __str__ function"""

        user = User.objects.create_user(username='username', password='password')
        user_profile = UserProfileModel.objects.create(account=user)

        notebook1 = NoteBookModel.objects.create(user=user_profile, title='notebook1')

        note1 = NoteModel.objects.create(notebook=notebook1, title='note1')

        self.assertEqual(note1.__str__(), note1.title)


class TestNoteAttachment(TestCase):
    """UnitTest for note attachments models"""

    def setUp(self):
        """Setup for unittest"""
        with open("media/.test", 'w+'):
            pass

    def test_note_attachment_slug_unique(self):
        """test for note attachment slug uniqueness"""

        user = User.objects.create_user(username='username', password='password')
        user_profile = UserProfileModel.objects.create(account=user)

        notebook = NoteBookModel.objects.create(user=user_profile, title='notebook')
        note = NoteModel.objects.create(notebook=notebook, title='note')

        attachment1 = NoteAttachmentModel.objects.create(note=note, file='.test')
        self.assertEqual(attachment1.slug, 'test')

        attachment2 = NoteAttachmentModel.objects.create(note=note, file='.test')
        self.assertEqual(attachment2.slug, 'test-2')
        self.assertNotEquals(attachment1.slug, attachment2.slug)

    def test_file_delete(self):
        """test for note attachment delete file from os function"""

        user = User.objects.create_user(username='username', password='password')
        user_profile = UserProfileModel.objects.create(account=user)

        notebook = NoteBookModel.objects.create(user=user_profile, title='group1')
        note = NoteModel.objects.create(notebook=notebook, title='note')

        attachment = NoteAttachmentModel.objects.create(note=note, file='.test')
        self.assertTrue(os.path.isfile(attachment.file.path))
        attachment.delete()

        self.assertFalse(os.path.isfile(attachment.file.path))
