#  Copyright (c) Code Written and Tested by Ahmed Emad in 14/03/2020, 22:30.

import os

from django.contrib.auth.models import User
from django.core.files import File
from django.test import TestCase

from core.serializers import UserProfileSerializer, NoteAttachmentSerializer


class TestUsers(TestCase):
    """UnitTest for users serializers"""

    def test_name_fields_required(self):
        """test for name fields requirements"""

        serializer = UserProfileSerializer(data={'username': 'username',
                                                 'password': 'super_secret'})
        self.assertFalse(serializer.is_valid())

        serializer = UserProfileSerializer(data={'username': 'username', 'first_name': 'first',
                                                 'last_name': 'last', 'password': 'super_secret'})
        self.assertTrue(serializer.is_valid())

    def test_username_unique(self):
        """test for username uniqueness"""

        User.objects.create(username='username', password='super_secret')
        serializer = UserProfileSerializer(data={'username': 'username', 'first_name': 'first',
                                                 'last_name': 'last', 'password': 'super_secret'})
        self.assertFalse(serializer.is_valid())

    def test_password_validation(self):
        """test for password validation"""

        # true
        serializer = UserProfileSerializer(data={'username': 'username', 'first_name': 'first',
                                                 'last_name': 'last', 'password': 'super_secret'})
        self.assertTrue(serializer.is_valid())

        # less than 8 chars
        serializer = UserProfileSerializer(data={'username': 'username', 'first_name': 'first',
                                                 'last_name': 'last', 'password': 'hi'})
        self.assertFalse(serializer.is_valid())

        # common password
        serializer = UserProfileSerializer(data={'username': 'username', 'first_name': 'first',
                                                 'last_name': 'last', 'password': 'password'})
        self.assertFalse(serializer.is_valid())

        # numbers only
        serializer = UserProfileSerializer(data={'username': 'username', 'first_name': 'first',
                                                 'last_name': 'last', 'password': '123456789'})
        self.assertFalse(serializer.is_valid())


class TestNoteAttachment(TestCase):
    """Unittest for note attachment"""

    def setUp(self):
        """setup for unittest"""

        # makes dummy file to test
        with open('media/.test', 'w+') as f:
            # 1 mb file
            f.write('a' * 10 ** 6)
            self.file = File(f)

        with open('media/.test2', 'w+') as f:
            # 7 mb file
            f.write('a' * 7 * 10 ** 6)
            self.file2 = File(f)

    def test_file_size(self):
        """test for file size validator"""

        # right
        serializer = NoteAttachmentSerializer(data={'file': self.file})
        self.assertTrue(serializer.is_valid())

        # wrong file size bigger than 2 mb
        serializer = NoteAttachmentSerializer(data={'file': self.file2})
        self.assertFalse(serializer.is_valid())

        # delete file from os after test
        os.remove(self.file.name)
        os.remove(self.file2.name)
