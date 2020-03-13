#  Copyright (c) Code Written and Tested by Ahmed Emad in 13/03/2020, 20:02.

import os
import re

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from core.models import UserProfileModel, NoteModel, NoteBookModel, NoteAttachmentModel


def _slug_strip(value):
    """removes the '-' separator from the end or start of the string"""
    return re.sub(r'^%s+|%s+$' % ('-', '-'), '', value)


def unique_slugify(instance, parent, value):
    """function used to give a unique slug to an instance"""

    slug = slugify(value)
    slug = slug[:255]  # limit its len to max_length of slug field

    slug = _slug_strip(slug)
    original_slug = slug

    queryset = instance.__class__.objects.filter(**{parent: getattr(instance, parent)}).all()

    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    _next = 2
    while not slug or queryset.filter(slug=slug):
        slug = original_slug
        end = '-%s' % _next
        if len(slug) + len(end) > 255:
            slug = slug[:255 - len(end)]
            slug = _slug_strip(slug)
        slug = '%s%s' % (slug, end)
        _next += 1

    return slug


@receiver(post_delete, sender=UserProfileModel)
def delete_user_account(sender, **kwargs):
    """The receiver called after a user profile is deleted
    to delete its one_to_one relation"""

    kwargs['instance'].account.delete()


@receiver(pre_save, sender=NoteBookModel)
def add_slug_to_notebook(sender, **kwargs):
    """The receiver called before a notebook is saved
    to give it a unique slug"""

    notebook = kwargs['instance']
    notebook.slug = unique_slugify(notebook, 'user', notebook.title)


@receiver(pre_save, sender=NoteModel)
def add_slug_to_note(sender, **kwargs):
    """The receiver called before a note is saved
    to give it a unique slug"""

    note = kwargs['instance']
    note.slug = unique_slugify(note, 'notebook', note.title)


@receiver(pre_save, sender=NoteAttachmentModel)
def add_slug_to_note_attachment(sender, **kwargs):
    """The receiver called before a note attachment is saved
    to give it a unique slug"""

    attachment = kwargs['instance']
    attachment.slug = unique_slugify(attachment, 'note', attachment.file.name)


@receiver(post_delete, sender=NoteAttachmentModel)
def delete_note_attachment_file(sender, **kwargs):
    """The receiver called after a note attachment is deleted
    to delete the file it pointes to in the filesystem"""

    attachment = kwargs['instance']
    if attachment.file:
        if os.path.isfile(attachment.file.path):
            os.remove(attachment.file.path)
