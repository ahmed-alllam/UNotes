#  Copyright (c) Code Written and Tested by Ahmed Emad in 14/03/2020, 22:30.
import random
import string

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from core.models import UserProfileModel, NoteBookModel, NoteModel, NoteAttachmentModel


class TestUsers(TestCase):
    """Unit Test for user's views"""

    def test_login(self):
        """Test for users login view"""

        user = User.objects.create_user(username='username', first_name='first',
                                        last_name='last', password='password')
        url = reverse('core:login')

        # user has no profile not valid
        response = self.client.post(url, {'username': 'username',
                                          'password': 'password'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

        UserProfileModel.objects.create(account=user)

        # wrong login password
        response = self.client.post(url, {'username': 'username',
                                          'password': 'a wrong password'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # right login
        response = self.client.post(url, {'username': 'username',
                                          'password': 'password'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # user already logged in
        response = self.client.post(url, {'username': 'username',
                                          'password': 'password'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_logout(self):
        """Test for users logout view"""

        user = User.objects.create_user(username='username', password='password')

        # user is logged in
        url = reverse('core:logout')
        self.client.force_login(user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

        # user is NOT logged in
        response = self.client.post(url)
        self.assertEqual(response.status_code, 401)

    def test_signup(self):
        """Test for users signup view"""
        url = reverse('core:signup')

        # right sign up
        response = self.client.post(url, {
            'first_name': 'my first name',
            'last_name': 'my last name',
            'username': 'username',
            'password': 'super_secret'
        }, content_type='application/json')

        self.assertEqual(response.status_code, 201)

        # already logged in
        response = self.client.post(url, {
            'username': 'username',
            'password': 'super_secret',
            'first_name': 'my first name',
            'last_name': 'my last name'
        }, content_type='application/json')

        self.assertEqual(response.status_code, 401)

        # creating user with a taken username
        self.client.logout()
        response = self.client.post(url, {
            'username': 'username',  # taken
            'password': 'super_secret',
            'first_name': 'my first name',
            'last_name': 'my last name'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # creating user with a non valid password
        response = self.client.post(url, {
            'username': 'no_taken_username',
            'password': '123',
            'first_name': 'my first name',
            'last_name': 'my last name'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)

    def test_get_user(self):
        """Test for users get view"""

        user = User.objects.create_user(username='username', password='password')
        UserProfileModel.objects.create(account=user)
        url = reverse('core:user-details')

        # note logged in
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        # right
        self.client.force_login(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_user(self):
        """Test for users update view"""

        user = User.objects.create_user(username='username', password='password')
        UserProfileModel.objects.create(account=user)
        url = reverse('core:user-details')

        # not logged in
        response = self.client.put(url, {
            'username': 'username',
            'password': 'super_secret',
            'first_name': 'my first name',
            'last_name': 'my last name'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 403)

        # wrong or uncompleted data
        self.client.force_login(user)
        response = self.client.put(url, {'first_name': 'my first name'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # uncompleted data passes the patch request right
        response = self.client.patch(url, {'first_name': 'my first name'},
                                     content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # wrong data with patch
        response = self.client.patch(url, {'username': 'username'},  # duplicate
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # right
        response = self.client.put(url, {
            'username': 'the_new_username',
            'password': 'super_secret',
            'first_name': 'my first name',
            'last_name': 'my last name'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        """Test for users delete view"""

        user = User.objects.create_user(username='username', password='password')
        UserProfileModel.objects.create(account=user)
        url = reverse('core:user-details')

        # not logged in
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

        # right
        self.client.force_login(user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(User.objects.filter(username='username').exists(), False)


class TestNoteBook(TestCase):
    """Unit Test for notebook views"""

    def test_list(self):
        """Test for notebook list view"""

        account = User.objects.create_user(username='username', password='password')
        UserProfileModel.objects.create(account=account)

        url = reverse('core:notebooks-list')

        # not logged
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        # right
        self.client.force_login(account)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        """test for notebook create view"""

        user = User.objects.create_user(username='username', password='password')
        UserProfileModel.objects.create(account=user)
        url = reverse('core:notebooks-list')

        # not logged
        response = self.client.post(url, {'title': 'title'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 403)

        # right
        self.client.force_login(user)
        response = self.client.post(url, {'title': 'title'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)

        # wrong data
        response = self.client.post(url, {},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_update(self):
        """test for notebook update view"""

        user = User.objects.create_user(username='username', password='password')
        user_profile = UserProfileModel.objects.create(account=user)
        NoteBookModel.objects.create(user=user_profile, title='title')
        url = reverse('core:notebooks-detail', kwargs={'slug': 'title'})

        # not logged
        response = self.client.put(url, {'title': 'title'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 403)

        # right
        self.client.force_login(user)
        response = self.client.put(url, {'title': 'title'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # wrong data for put
        response = self.client.put(url, {},  # missing attrs
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # wrong notebook slug
        url = reverse('core:notebooks-detail', kwargs={'slug': 'wrong'})
        response = self.client.put(url, {'title': 'title'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_delete(self):
        """test for notebook delete view"""

        user = User.objects.create_user(username='username', password='password')
        user_profile = UserProfileModel.objects.create(account=user)
        NoteBookModel.objects.create(user=user_profile, title='title')

        url = reverse('core:notebooks-detail', kwargs={'slug': 'title'})

        # not logged
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

        # right
        self.client.force_login(user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

        # wrong notebook slug
        url = reverse('core:notebooks-detail', kwargs={'slug': 'wrong'})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)


class TestNote(TestCase):
    """Unit Test for note views"""

    def setUp(self):
        """setup for unittest"""
        self.account = User.objects.create_user(username='username', password='password')
        user_profile = UserProfileModel.objects.create(account=self.account)
        self.notebook = NoteBookModel.objects.create(user=user_profile, title='title')

    def test_list(self):
        """Test for note list view"""

        NoteModel.objects.create(notebook=self.notebook, title='title')
        url = reverse('core:notes-list', kwargs={'notebook_slug': 'title'})

        # not logged
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        # logged in as a user that has no valid user profile
        user2 = User.objects.create_user(username='username2', password='password')
        self.client.force_login(user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        # right
        self.client.force_login(self.account)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # wrong slug
        url = reverse('core:notes-list', kwargs={'notebook_slug': 'wrong'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_get(self):
        """Test for note get view"""

        NoteModel.objects.create(notebook=self.notebook, title='title')
        url = reverse('core:notes-detail', kwargs={'notebook_slug': 'title', 'slug': 'title'})

        # not logged
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        # right
        self.client.force_login(self.account)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # wrong note slug
        url = reverse('core:notes-detail', kwargs={'notebook_slug': 'title', 'slug': 'wrong'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        # wrong notebook slug
        url = reverse('core:notes-detail', kwargs={'notebook_slug': 'wrong', 'slug': 'title'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create(self):
        """Test for note create view"""

        url = reverse('core:notes-list', kwargs={'notebook_slug': 'title'})

        # not logged
        response = self.client.post(url, {'title': 'title'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 403)

        # right
        self.client.force_login(self.account)
        response = self.client.post(url, {'title': 'title'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)

        # wrong data
        response = self.client.post(url, {},  # missing attrs
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # wrong notebook slug
        url = reverse('core:notes-list', kwargs={'notebook_slug': 'wrong'})
        response = self.client.post(url, {'title': 'title'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_update(self):
        """Test for note update view"""

        NoteModel.objects.create(notebook=self.notebook, title='title')
        url = reverse('core:notes-detail', kwargs={'notebook_slug': 'title', 'slug': 'title'})

        # not logged
        response = self.client.put(url, {'title': 'title'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 403)

        # right
        self.client.force_login(self.account)
        response = self.client.put(url, {'title': 'title'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # wrong data for put
        response = self.client.put(url, {},  # missing attrs
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # wrong data for patch
        response = self.client.patch(url, {'title': ''.join(random.choice(string.ascii_lowercase) for i in range(300))},
                                     # title bigger than 255
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # right for patch
        response = self.client.patch(url, {'title': 'title'},
                                     content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # wrong note slug
        url = reverse('core:notes-detail', kwargs={'notebook_slug': 'title', 'slug': 'wrong'})

        response = self.client.put(url, {'title': 'title'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 404)

        # wrong notebook slug
        url = reverse('core:notes-detail', kwargs={'notebook_slug': 'wrong', 'slug': 'title'})
        response = self.client.put(url, {'title': 'title'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_delete(self):
        """Test for note delete view"""

        NoteModel.objects.create(notebook=self.notebook, title='title')
        url = reverse('core:notes-detail', kwargs={'notebook_slug': 'title', 'slug': 'title'})

        # not logged in
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

        # right
        self.client.force_login(self.account)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

        # wrong note slug
        url = reverse('core:notes-detail', kwargs={'notebook_slug': 'title', 'slug': 'wrong'})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

        # wrong notebook slug
        url = reverse('core:notes-detail', kwargs={'notebook_slug': 'wrong', 'slug': 'title'})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)


class TestNoteAttachment(TestCase):
    """Unit Test for note attachment views"""

    def setUp(self):
        """set up for unittest"""

        self.account = User.objects.create_user(username='username', password='password')
        user = UserProfileModel.objects.create(account=self.account)
        notebook = NoteBookModel.objects.create(user=user, title='title')
        self.note = NoteModel.objects.create(notebook=notebook, title='title')

    def img_upload(self):
        """returns a file object"""
        file_path = 'media/.test'

        f = open(file_path, 'wb+')
        f.write(b'a')
        f.seek(0)

        return SimpleUploadedFile(name='test_img.jpg',
                                  content=f.read(),
                                  content_type='image/jpg')

    def delete_test_files(self):
        """deletes generated test files"""

        for attachment in self.note.attachments.all():
            attachment.delete()

    def test_create(self):
        """test for note attachment create view"""

        url = reverse('core:attachments-list', kwargs={'notebook_slug': 'title', 'note_slug': 'title'})

        # not logged
        response = self.client.post(url, {'file': self.img_upload()})
        self.assertEqual(response.status_code, 403)

        # right
        self.client.force_login(self.account)
        response = self.client.post(url, {'file': self.img_upload()})
        self.assertEqual(response.status_code, 201)

        # wrong data
        response = self.client.post(url, {})  # missing attrs
        self.assertEqual(response.status_code, 400)

        # wrong notebook slug
        url = reverse('core:attachments-list', kwargs={'notebook_slug': 'wrong', 'note_slug': 'title'})
        response = self.client.post(url, {'file': self.img_upload()})
        self.assertEqual(response.status_code, 404)

        # wrong note slug
        url = reverse('core:attachments-list', kwargs={'notebook_slug': 'title', 'note_slug': 'wrong'})
        response = self.client.post(url, {'file': self.img_upload()})
        self.assertEqual(response.status_code, 404)

        self.delete_test_files()

    def test_delete(self):
        """test for note attachment delete view"""

        NoteAttachmentModel.objects.create(note=self.note, file=self.img_upload())

        url = reverse('core:attachments-detail', kwargs={'notebook_slug': 'title', 'note_slug': 'title',
                                                         'slug': 'test_imgjpg'})

        # not logged
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

        # right
        self.client.force_login(self.account)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

        # wrong notebook slug
        url = reverse('core:attachments-detail', kwargs={'notebook_slug': 'wrong', 'note_slug': 'title',
                                                         'slug': 'test_imgjpg'})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

        # wrong note slug
        url = reverse('core:attachments-detail', kwargs={'notebook_slug': 'title', 'note_slug': 'wrong',
                                                         'slug': 'test_imgjpg'})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

        # wrong attachment slug
        url = reverse('core:attachments-detail', kwargs={'notebook_slug': 'title', 'note_slug': 'title',
                                                         'slug': 'wrong'})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

        self.delete_test_files()
