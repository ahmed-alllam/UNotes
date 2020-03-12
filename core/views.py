#  Copyright (c) Code Written and Tested by Ahmed Emad in 12/03/2020, 20:23.

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from core.models import NoteBookModel, NoteModel, NoteAttachmentModel
from core.permissions import UserProfilePermissions, NoteBookPermissions, NotePermissions, NoteAttachmentPermissions
from core.serializers import UserProfileSerializer, NoteBookSerializer, NoteSerializer, NoteAttachmentSerializer, \
    NoteDetailSerializer


@api_view(['POST'])
def user_login(request):
    """View for logging the users in"""

    if request.user.is_authenticated:
        return Response('User already logged in', status=status.HTTP_401_UNAUTHORIZED)

    username = request.data['username']
    password = request.data['password']

    user = authenticate(username=username, password=password)

    if user and hasattr(user, 'profile'):
        login(request, user)
        return Response('Logged In Successfully')
    else:
        return Response('Wrong Username or Password', status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_logout(request):
    """View for logging the users in"""

    if request.user.is_authenticated:
        logout(request)
        return Response('Logged Out Successfully')
    return Response('Your are not logged in', status=status.HTTP_401_UNAUTHORIZED)


class UserProfileView(viewsets.ViewSet):
    """View for the user profile.
    Retrieves, creates, Updates and Deletes a User Profile.
    """

    permission_classes = (UserProfilePermissions,)
    serializer_class = UserProfileSerializer

    def retrieve(self, request):
        """Retrieves a user profile by its username
        Checks if a user profile with this username exist,
        if not, returns HTTP 404 Response.
        Arguments:
            request: the request data sent by the user,
                     used to get the user profile
        Returns:
            HTTP 403 if user is not logged in,
            if not, returns HTTP 200 Response with the profile's JSON data.
        """
        user_profile = request.user.profile
        serializer = self.serializer_class(user_profile)
        return Response(serializer.data)

    def create(self, request):
        """Creates A new user profile and Logs it In.
        Checks if user is authenticated if true, return HTTP 401 Response,
        then it Validates the post data if not valid,
        return HTTP 400 Response, then creates the user and logs him in,
        and returns 201 Response.
        Arguments:
            request: the request data sent by the user, it is used
                     to get the post data from it to get validated and created,
                     and to log the user in.
        Returns:
             HTTP 400 Response if data is not valid,
             HTTP 401 Response if user is already logged in,
             HTTP 201 Response with the JSON data of the created profile.
        """

        if not request.user.is_authenticated:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                user_profile = serializer.save()
                login(request, user_profile.account)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request):
        """Completely Updates the user profile.
        Arguments:
            request: the request data sent by the user, it is used
                     to get the user's profile
        Returns:
             HTTP 400 Response if the data is not
             valid with the errors,
             HTTP 403 Response if the user is not
             logged in,
             if not returns HTTP 200 Response with the update JSON data.
        """

        user_profile = request.user.profile
        serializer = self.serializer_class(user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            update_session_auth_hash(request, user_profile.account)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request):
        """Partially Updates the user profile.
        Arguments:
            request: the request data sent by the user, it is used
                     to get the user's profile
        Returns:
             HTTP 400 Response if the data is not
             valid with the errors,
             HTTP 403 Response if the user is not
             logged in,
             if not returns HTTP 200 Response with the update JSON data.
        """

        user_profile = request.user.profile
        serializer = self.serializer_class(user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            update_session_auth_hash(request, user_profile.account)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request):
        """Deletes the user profile.
        Arguments:
            request: the request data sent by the user, it is used
                     to get the user's profile
        Returns:
            HTTP 403 Response if the user is not logged in,
            if not returns HTTP 204 Response with no content.
        """

        user_profile = request.user.profile
        user_profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NoteBookView(viewsets.ViewSet):
    """View for the user Notebooks.
    Lists, Creates, Updates and Deletes a note book.
    """

    permission_classes = (NoteBookPermissions,)
    serializer_class = NoteBookSerializer

    def list(self, request):
        """Lists all notebooks the user has.
        Arguments:
            request: the request data sent by the user, it is used
                     to get the user's profile.
        Returns:
            HTTP 403 Response if the user is
            not logged in,
            HTTP 200 Response with all notebooks in
            the user's profile in JSON.
        """
        user = request.user.profile
        queryset = user.notebooks

        paginator = LimitOffsetPagination()
        paginator.default_limit = 10
        paginator.max_limit = 100
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)

        return Response(data={'limit': paginator.limit, 'offset': paginator.offset,
                              'count': paginator.count, 'notebooks': serializer.data})

    def create(self, request):
        """Creates a new notebook and adds it to the user's list.
        Arguments:
            request: the request data sent by the user, it is used
                     to get the user's profile
        Returns:
            HTTP 403 Response if the user is
            not logged in,
            HTTP 400 Response if the data is not valid, if not,
            returns HTTP 201 Response with the notebook's JSON data.
        """
        user = request.user.profile
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Completely Updates a certain notebook from the user's list.
        Arguments:
            request: the request data sent by the user, it is used
                     to get the user profile.
            pk: the sort of the notebook that the user wants to change,
                it should by an integer.
        Returns:
            HTTP 404 Response if the notebook is not found,
            HTTP 403 Response if the user is
            not logged in,
            HTTP 400 Response if the data is not valid with the errors,
            if not returns HTTP 200 Response with the update JSON data.
        """
        user = request.user.profile
        notebook = get_object_or_404(NoteBookModel, sort=pk, user=user)
        serializer = self.serializer_class(notebook, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Deletes a certain notebook from the user's list.
        Arguments:
            request: the request data sent by the user, it is used
                     to get the user profile
            pk: the sort of the notebook that the user wants to delete,
                it should by an integer.
        Returns:
            HTTP 404 Response if the notebook is not found
            HTTP 403 Response if the user is
            not logged in,
            if not, returns HTTP 204 Response with no content.
        """
        user = request.user.profile
        notebook = get_object_or_404(NoteBookModel, sort=pk, user=user)
        notebook.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NoteView(viewsets.ViewSet):
    """View for the user note.
    Lists, Creates, Updates and Deletes a note.
    """

    permission_classes = (NotePermissions,)
    serializer_class = NoteDetailSerializer

    def list(self, request, notebook_sort=None):
        """Lists all notes the user has inside a notebook.
        Arguments:
            request: the request data sent by the user, it is used
                     to get the user's profile.
            notebook_sort: the sort of the notebook that
                        the requested notes are in.
        Returns:
            HTTP 404 if notebook is not found
            HTTP 403 Response if the user is
            not logged in,
            HTTP 200 Response with all notes in JSON.
        """
        user = request.user.profile
        notebook = get_object_or_404(NoteBookModel, user=user, sort=notebook_sort)
        queryset = notebook.notes

        paginator = LimitOffsetPagination()
        paginator.default_limit = 30
        paginator.max_limit = 100
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = NoteSerializer(paginated_queryset, many=True)

        return Response(data={'limit': paginator.limit, 'offset': paginator.offset,
                              'count': paginator.count, 'notes': serializer.data})

    def retrieve(self, request, notebook_sort=None, pk=None):
        """Retrieves a certain note from the user's list
        Arguments:
            request: the request data sent by the user, it is used
                     get the user profile.
            notebook_sort: the sort of the notebook that
                        the requested note is in.
            pk: the sort of the note that the user want info about,
                it should by an integer.
        Returns:
            HTTP 403 Response if the user is
            not logged in,
            HTTP 404 Response if note is not found, if not,
            returns HTTP 200 Response with the note's JSON data.
        """
        user = request.user.profile
        note = get_object_or_404(NoteModel, sort=pk, notebook__sort=notebook_sort,
                                 notebook__user=user)
        serializer = self.serializer_class(note)
        return Response(serializer.data)

    def create(self, request, notebook_sort=None):
        """Creates a new note and adds it to the user's list.
        Arguments:
            request: the request data sent by the user, it is used
                     get the user profile.
            notebook_sort: the sort of the notebook that
                        the created note will be in.
        Returns:
            HTTP 403 Response if the user is
            not logged in,
            HTTP 404 if notebook is not found,
            HTTP 400 Response if the data is not valid, if not,
            returns HTTP 201 Response with the note's JSON data.
        """
        user = request.user.profile
        notebook = get_object_or_404(NoteBookModel, user=user,
                                     sort=notebook_sort)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(notebook=notebook)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, notebook_sort=None, pk=None):
        """Completely Updates a certain note from the user's list.
        Arguments:
            request: the request data sent by the user, it is used
                     to get the user's profile.
            notebook_sort: the sort of the notebook that
                        the created note is in.
            pk: the sort of the note that the user wants to change,
                it should by an integer.
        Returns:
            HTTP 403 Response if the user is
            not logged in,
            HTTP 400 Response if the data is not valid with the errors,
            HTTP 404 Response if the note is not found
            if not returns HTTP 200 Response with the update JSON data.
        """
        user = request.user.profile
        note = get_object_or_404(NoteModel, sort=pk, notebook__sort=notebook_sort,
                                 notebook__user=user)
        serializer = self.serializer_class(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, notebook_sort=None, pk=None):
        """Partially Updates a certain note from the user's list.
        Arguments:
            request: the request data sent by the user, it is used
                     to get the user's profile.
            notebook_sort: the sort of the notebook that
                        the created note is in.
            pk: the sort of the note that the user wants to change,
                it should by an integer.
        Returns:
            HTTP 403 Response if the user is
            not logged in,
            HTTP 400 Response if the data is not valid with the errors,
            HTTP 404 Response if the note is not found
            if not returns HTTP 200 Response with the update JSON data.
        """
        user = request.user.profile
        note = get_object_or_404(NoteModel, sort=pk, notebook__sort=notebook_sort,
                                 notebook__user=user)
        serializer = self.serializer_class(note, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, notebook_sort=None, pk=None):
        """Deletes a certain note from the user's list.
        Arguments:
            request: the request data sent by the user, it is used
                     to check the user's permissions
            notebook_sort: the sort of the notebook that
                           the note is in.
            pk: the id of the note that the user wants to delete,
                it should by an integer.
        Returns:
            HTTP 404 Response if the note is not found
            HTTP 403 Response if the user is
            not logged in,
            if not, returns HTTP 204 Response with no content.
        """
        user = request.user.profile
        note = get_object_or_404(NoteModel, sort=pk, notebook__sort=notebook_sort,
                                 notebook__user=user)
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NoteAttachmentView(viewsets.ViewSet):
    """View for the note attachment.
    Creates and Deletes a note attachment.
    """

    permission_classes = (NoteAttachmentPermissions,)
    serializer_class = NoteAttachmentSerializer

    def create(self, request, notebook_sort=None, note_sort=None):
        """Creates a new note attachment and adds it to the note's list.
        Arguments:
            request: the request data sent by the user, it is used
                     to get the user's profile
            notebook_sort: the notebook sort that the note is in
            note_sort: the note sort that the attachment will be in
        Returns:
            HTTP 403 Response if the user is
            not logged in,
            HTTP 404 if note is not found,
            HTTP 400 Response if the data is not valid, if not,
            returns HTTP 201 Response with the note attachment's JSON data.
        """
        user = request.user.profile
        note = get_object_or_404(NoteModel, notebook__sort=notebook_sort,
                                 notebook__user=user, sort=note_sort)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(note=note)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, notebook_sort=None, note_sort=None, pk=None):
        """Deletes a certain note attachment from the note's attachments list.
        Arguments:
            request: the request data sent by the user, it is used
                     to get the user's profile
            notebook_sort: the notebook sort that the note is in
            note_sort: the note sort that the attachment is in
            pk: the id of the note attachment that the user wants to delete,
                it should by an integer.
        Returns:
            HTTP 404 Response if the note attachment is not found
            HTTP 403 Response if the user is
            not logged in,
            if not, returns HTTP 204 Response with no content.
        """
        user = request.user.profile
        attachment = get_object_or_404(NoteAttachmentModel, note__notebook__user=user,
                                       note__notebook__sort=notebook_sort, note__sort=note_sort, sort=pk)
        attachment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
