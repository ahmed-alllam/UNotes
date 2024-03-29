#  Copyright (c) Code Written and Tested by Ahmed Emad in 13/03/2020, 20:02.

import uuid

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


def users_upload(instance, filename):
    """Gives a unique path to the saved user photo in models.
    Arguments:
        instance: the model itself, it is not used in this
                  function but it's required by django.
        filename: the name of the photo sent by user, it's
                  used here to get the format of the photo.
    Returns:
        The unique path that the photo will be stored in the DB.
    """
    return 'users/{0}{1}'.format(uuid.uuid4().hex, filename)


def attachment_upload(instance, filename):
    """Gives a unique path to the saved attachment file in models.
    Arguments:
        instance: the model itself, it is not used in this
                  function but it's required by django.
        filename: the name of the file sent by user, it's
                  used here to get the format of the file.
    Returns:
        The unique path that the file will be stored in the DB.
    """
    return 'attachments/{0}{1}'.format(uuid.uuid4().hex, filename)


class UserProfileModel(models.Model):
    """The Model of the User Profile."""

    account = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_photo = models.ImageField(upload_to=users_upload, null=True)

    def __str__(self):
        return self.account.username


class NoteBookModel(models.Model):
    """The Model of the NoteBooks."""

    slug = models.SlugField(max_length=255)
    user = models.ForeignKey(UserProfileModel, on_delete=models.CASCADE, related_name='notebooks')
    title = models.CharField(max_length=255)

    class Meta:
        unique_together = ("user", "slug")

    def __str__(self):
        return self.title


class NoteModel(models.Model):
    """The Model of the Note."""

    slug = models.SlugField(max_length=255)
    notebook = models.ForeignKey(NoteBookModel, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=255)
    text = models.TextField(blank=True)

    class Meta:
        unique_together = ("notebook", "slug")

    def __str__(self):
        return self.title


def filesize(value):
    """Model Validator for file size limit"""
    limit = 2 * 1000 * 1000
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MB.')


class NoteAttachmentModel(models.Model):
    """an alias to filefield to enable
    having multiple file attachments in a Note"""

    slug = models.SlugField(max_length=255)
    note = models.ForeignKey(NoteModel, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to=attachment_upload, validators=[filesize])

    class Meta:
        unique_together = ("note", "slug")
