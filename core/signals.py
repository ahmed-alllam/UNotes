#  Copyright (c) Code Written and Tested by Ahmed Emad in 09/03/2020, 16:03.

import os

from django.db.models import F
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from core.models import UserProfileModel, NoteModel, NoteBookModel, NoteAttachmentModel


@receiver(post_delete, sender=UserProfileModel)
def delete_user_account(sender, **kwargs):
    """The receiver called after a user profile is deleted
    to delete its one_to_one relation"""

    kwargs['instance'].account.delete()


@receiver(pre_save, sender=NoteBookModel)
def add_sort_to_note_book(sender, **kwargs):
    """The receiver called before a notebook is saved
    to give it a unique sort"""

    notebook = kwargs['instance']
    if not notebook.pk:
        latest_sort = NoteBookModel.objects.filter(user=notebook.user).count()
        notebook.sort = latest_sort + 1


@receiver(pre_save, sender=NoteModel)
def add_sort_to_note(sender, **kwargs):
    """The receiver called before a note is saved
    to give it a unique sort"""

    note = kwargs['instance']
    if not note.pk:
        latest_sort = NoteModel.objects.filter(notebook=note.note_book).count()
        note.sort = latest_sort + 1


@receiver(pre_save, sender=NoteAttachmentModel)
def add_sort_to_note_attachment(sender, **kwargs):
    """The receiver called before a note attachment is saved
    to give it a unique sort"""

    attachment = kwargs['instance']
    if not attachment.pk:
        latest_sort = NoteAttachmentModel.objects.filter(note=attachment.note).count()
        attachment.sort = latest_sort + 1


@receiver(post_delete, sender=NoteBookModel)
def resort_notebooks(sender, **kwargs):
    """The receiver called after a note book is deleted
    to resort them"""

    notebook = kwargs['instance']
    notebook.user.notebooks.filter(sort__gt=notebook.sort).update(sort=F('sort') - 1)


@receiver(post_delete, sender=NoteModel)
def resort_notes(sender, **kwargs):
    """The receiver called after a note is deleted
    to resort them"""

    note = kwargs['instance']
    note.notebook.notes.filter(sort__gt=note.sort).update(sort=F('sort') - 1)


@receiver(post_delete, sender=NoteAttachmentModel)
def resort_note_attachment(sender, **kwargs):
    """The receiver called after a note attachment is deleted
    to resort them"""

    attachment = kwargs['instance']
    attachment.note.attachments.filter(sort__gt=attachment.sort).update(sort=F('sort') - 1)


@receiver(post_delete, sender=NoteAttachmentModel)
def delete_note_attachment_file(sender, **kwargs):
    """The receiver called after a note attachment is deleted
    to delete the file it pointes to in the filesystem"""

    attachment = kwargs['instance']
    if attachment.file:
        if os.path.isfile(attachment.file.path):
            os.remove(attachment.file.path)
