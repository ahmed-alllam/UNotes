#  Copyright (c) Code Written and Tested by Ahmed Emad in 09/03/2020, 23:56.

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from core.models import UserProfileModel, NoteModel, NoteBookModel, NoteAttachmentModel


class UserProfileSerializer(serializers.ModelSerializer):
    """The serializer for the user profile model"""

    first_name = serializers.CharField(source='account.first_name', label=_('first name'),
                                       max_length=30)
    last_name = serializers.CharField(source='account.last_name', label=_('last name'),
                                      max_length=30)
    username = serializers.CharField(source='account.username', label=_('username'),
                                     max_length=150,
                                     validators=[UnicodeUsernameValidator(),
                                                 UniqueValidator(queryset=User.objects.all())],
                                     help_text=_(
                                         'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
                                     error_messages={
                                         'unique': _("A user with that username already exists.")
                                     })
    password = serializers.CharField(source='account.password', write_only=True, label=_('password'),
                                     max_length=128, validators=[validate_password])

    class Meta:
        model = UserProfileModel
        fields = ('first_name', 'last_name', 'username', 'password', 'profile_photo')

    def create(self, validated_data):
        """Creates a new user profile from the request's data"""

        account_data = validated_data.pop('account')
        account = User(**account_data)
        account.set_password(account.password)
        account.save()

        user_profile = UserProfileModel.objects.create(account=account, **validated_data)
        return user_profile

    def update(self, instance, validated_data):
        """Updates a certain user profile from the request's data"""

        instance.profile_photo = validated_data.get('profile_photo', instance.profile_photo)
        instance.save()

        account_data = validated_data.pop('account', {})
        account = instance.account
        account.first_name = account_data.get('first_name', account.first_name)
        account.last_name = account_data.get('last_name', account.last_name)
        account.username = account_data.get('username', account.username)
        if account_data.get('password', None) is not None:
            account.set_password(account_data.get('password'))
        account.save()

        return instance


class NoteAttachmentSerializer(serializers.ModelSerializer):
    """The serializer for the note attachment model"""

    class Meta:
        model = NoteAttachmentModel
        fields = ('sort', 'file')
        extra_kwargs = {
            'sort': {'read_only': True}
        }


class NoteDetailSerializer(serializers.ModelSerializer):
    """The Detailed serializer for the note model"""

    attachments = NoteAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = NoteModel
        fields = ('sort', 'title', 'text', 'attachments')
        extra_kwargs = {
            'sort': {'required': False}
        }

    def validate_sort(self, sort):
        """validator for sort field"""

        if not self.instance:
            raise serializers.ValidationError(_("sort can't be specified before creation"))
        if sort > self.instance.notebook.notes.count() or sort < 1:
            raise serializers.ValidationError(_("invalid sort number"))
        return sort

    def update(self, instance, validated_data):
        """updates a note"""

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('text', instance.description)

        if validated_data.get('sort', None):
            old_sort = instance.sort
            new_sort = validated_data.get('sort')

            instance.sort = None
            instance.save()

            if new_sort - old_sort > 0:
                notes = instance.notebook.notes.filter(sort__gt=old_sort,
                                                       sort__lte=new_sort,
                                                       sort__isnull=False)
                for note in notes:
                    note.sort -= 1
                    note.save()

            elif new_sort - old_sort < 0:
                notes = instance.notebook.notes.filter(sort__lt=old_sort,
                                                       sort__gte=new_sort,
                                                       sort__isnull=False).order_by('-sort')
                for note in notes:
                    note.sort += 1
                    note.save()

            instance.sort = new_sort
            instance.save()

        return instance


class NoteSerializer(serializers.ModelSerializer):
    """The read-only serializer for the note model"""

    class Meta:
        model = NoteModel
        fields = ('sort', 'title')


class NoteBookSerializer(serializers.ModelSerializer):
    """The serializer for the notebook model"""

    notes = NoteSerializer(many=True, read_only=True)

    class Meta:
        model = NoteBookModel
        fields = ('sort', 'title', 'notes')
        extra_kwargs = {
            'sort': {'required': False}
        }

    def validate_sort(self, sort):
        """validator for sort field"""

        if not self.instance:
            raise serializers.ValidationError(_("sort can't be specified before creation"))
        if sort > self.instance.user.notebooks.count() or sort < 1:
            raise serializers.ValidationError(_("invalid sort number"))
        return sort

    def update(self, instance, validated_data):
        """updates a notebook"""

        instance.title = validated_data.get('title', instance.title)

        if validated_data.get('sort', None):
            old_sort = instance.sort
            new_sort = validated_data.get('sort')

            instance.sort = None
            instance.save()

            if new_sort - old_sort > 0:
                notebooks = instance.user.notebooks.filter(sort__gt=old_sort,
                                                           sort__lte=new_sort,
                                                           sort__isnull=False)
                for notebook in notebooks:
                    notebook.sort -= 1
                    notebook.save()

            elif new_sort - old_sort < 0:
                notebooks = instance.user.notebooks.filter(sort__lt=old_sort,
                                                           sort__gte=new_sort,
                                                           sort__isnull=False).order_by('-sort')
                for notebook in notebooks:
                    notebook.sort += 1
                    notebook.save()

            instance.sort = new_sort
            instance.save()

        return instance
