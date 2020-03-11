#  Copyright (c) Code Written and Tested by Ahmed Emad in 11/03/2020, 12:21.

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.serializers import UserProfileSerializer


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

    # permission_classes = (UserProfilePermissions,)
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
