#  Copyright (c) Code Written and Tested by Ahmed Emad in 13/03/2020, 20:02.

# Generated by Django 3.0.3 on 2020-03-13 17:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0002_auto_20200309_1413'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='noteattachmentmodel',
            options={},
        ),
        migrations.AlterModelOptions(
            name='notebookmodel',
            options={},
        ),
        migrations.AlterModelOptions(
            name='notemodel',
            options={},
        ),
        migrations.AddField(
            model_name='noteattachmentmodel',
            name='slug',
            field=models.SlugField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notebookmodel',
            name='slug',
            field=models.SlugField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notemodel',
            name='slug',
            field=models.SlugField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='noteattachmentmodel',
            unique_together={('note', 'slug')},
        ),
        migrations.AlterUniqueTogether(
            name='notebookmodel',
            unique_together={('user', 'slug')},
        ),
        migrations.AlterUniqueTogether(
            name='notemodel',
            unique_together={('notebook', 'slug')},
        ),
        migrations.RemoveField(
            model_name='noteattachmentmodel',
            name='sort',
        ),
        migrations.RemoveField(
            model_name='notebookmodel',
            name='sort',
        ),
        migrations.RemoveField(
            model_name='notemodel',
            name='sort',
        ),
    ]
