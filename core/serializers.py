#  Copyright (c) Code Written and Tested by Ahmed Emad in 13/03/2020, 20:02.

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
        fields = ('slug', 'file')
        extra_kwargs = {
            'slug': {'read_only': True}
        }


class NoteDetailSerializer(serializers.ModelSerializer):
    """The Detailed serializer for the note model"""

    attachments = NoteAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = NoteModel
        fields = ('slug', 'title', 'text', 'attachments')
        extra_kwargs = {
            'slug': {'read_only': True}
        }


class NoteSerializer(serializers.ModelSerializer):
    """The read-only serializer for the note model"""

    class Meta:
        model = NoteModel
        fields = ('slug', 'title')


class NoteBookSerializer(serializers.ModelSerializer):
    """The serializer for the notebook model"""

    notes = NoteSerializer(many=True, read_only=True)

    class Meta:
        model = NoteBookModel
        fields = ('slug', 'title', 'notes')
        extra_kwargs = {
            'slug': {'read_only': True}
        }
