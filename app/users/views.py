from socket import timeout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from appconf import settings
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string, get_template
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.cache import cache
from django.contrib.auth import get_user_model
import uuid
import os


from core.models import User
from .serializers import UserSerializer



class RegisterView(APIView):
    """View of Creation of the user in database"""

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        """create a user in the database"""

        try:
            data = request.data

            if data["password"] == data["re_password"]:

                if len(data["password"]) >= 8:

                    # We check if the user already exists in the database.
                    if not get_user_model().objects.filter(email = data["email"]).exists():

                        # Before creating a user we must retrieve re_password from the
                        # data dictionnary since re_password is not a model attribute of
                        # User model
                        data.pop("re_password")

                        # We create the user
                        User.objects.create_user(**data)

                        # We check if the user just created is well in database.
                        if get_user_model().objects.filter(email = data["email"]).exists():

                            new_user = get_user_model().objects.get(email = data["email"] )

                            serializer = UserSerializer(new_user, many = False)
                            message = {
                                "feedbackResponse": "User has been created successfully",
                                "dataResponse": serializer.data
                            }
                            return Response(
                                message,
                                status = status.HTTP_201_CREATED
                            )
                        else:
                            message = {"feedbackResponse": "Problem occurs with the database"}
                            return Response(
                                message,
                                status = status.HTTP_400_BAD_REQUEST
                            )
                    else:
                        message = {"feedbackResponse": "A user with this email already exists"}
                        return Response(
                            message,
                            status = status.HTTP_400_BAD_REQUEST
                        )

                else:
                    return Response(
                        {"feedbackResponse":"password must be at least 8 character of length"},
                        status = status.HTTP_400_BAD_REQUEST
                    )

            else:
                return Response(
                    {"feedbackResponse":"passwords do not match"},
                    status = status.HTTP_400_BAD_REQUEST
                )

        except:
            return Response(
                {"feedbackResponse":"Quelque chose a mal fonctionné lors de l'enregistrement"},
                status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RegisterEmailVerification(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            data = request.data
            frontend_id = int(data["user_hash_id"])
            frontend_token = data["token"]

            if cache.get("redis_user_identifier"):

                # We retrieve user_hash_id and token from redis cache
                identifier = cache.get("redis_user_identifier")
                redis_user_id = int(identifier["user_hash_id"])
                redis_token = identifier["token"]

                if User.objects.get(id = frontend_id):

                    # We retrieve the id of user from database who corresponds to frontend_id
                    user =  User.objects.get(id = frontend_id)
                    user_id = user.id

                    # We make comparison between (user_id and user_hash_id) and (token and redis_token)
                    if user_id == redis_user_id and frontend_token == redis_token:
                        user.email_verified = True
                        user.save()

                        return Response(
                            {"feedbackResponse":"Your email Has been Verified", "success": True},
                            status = status.HTTP_200_OK
                        )
                    else:
                        return Response(
                            {"feedbackResponse":"You don't use token we have sent to you", "success": False},
                            status = status.HTTP_400_BAD_REQUEST
                        )
                else:
                    return Response(
                        {"feedbackResponse": "You are not in our database. Please try to register first", "success": False},
                        status = status.HTTP_400_BAD_REQUEST
                    )

            else:
                return Response(
                    {"feedbackResponse":"Your Link expired. Please try to claim a new verify link", "success": False},
                    status = status.HTTP_400_BAD_REQUEST
                )

        except:
            message = {"feedbackResponse": "Something went wrong when trying to verify your email. Please try again later","success": False}
            return Response(message, status = status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoadUserView(APIView):

    def get(self, request, format = None):

        try:
            user = request.user
            serializer = UserSerializer(user)

            message  = {"dataResponse":serializer.data,"feedbackResponse":"Successfully retrieved data"}

            return Response(
                message,
                status = status.HTTP_200_OK
            )
        except:
            message = {"feedbackResponse":"Something went wrong when retrieving user"}
            return Response(
                message,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GetUsers(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format = None):
        try:
            users = User.objects.all()
            serializer = UserSerializer(users, many = True)

            if len(serializer.data) == 0:
                message = {
                    "feedbackResponse":"No users found",
                    "dataResponse": serializer.data
                }
                return Response(message, status = status.HTTP_404_NOT_FOUND)
            else:
                message = {
                    "feedbackResponse":"Users retrieved successfully",
                    "dataResponse": serializer.data
                }
                return Response(message, status = status.HTTP_200_OK)

        except:
            message = {"feedbackResponse": "something went wrong when retrieving jobs"}
            return Response(message, status = status.HTTP_500_INTERNAL_SERVER_ERROR)


####################################    UPDATE A USER   ##################################

class UpdateUserView(APIView):
    """View to Update a user."""

    def post(self, request):
        """Update user by giving an id as a params and data as a body of request."""
        try:
            user_id = int(request.query_params.get("userId"))
            data = request.data

            if get_user_model().objects.filter(id = user_id).exists():

                get_user_model().objects.filter(id = user_id).update(
                    first_name = data["first_name"],
                    last_name = data["last_name"],
                    email = data["email"],
                    phone = data["phone"],
                    street_number = data["street_number"],
                    address = data["address"],
                    postal_code = data["postal_code"],
                    town = data["town"],
                    province = data["province"],
                    country = data["country"],
                )

                user = get_user_model().objects.get(id = user_id)

                serializer = UserSerializer(user, many = False)

                message = {
                    "feedbackResponse": "User has been updated successfully",
                    "dataResponse":serializer.data
                }
                return Response(message, status = status.HTTP_200_OK)
            else:
                message = {"feedbackResponse": "The user does not exists in the database."}
                return Response(message, status = status.HTTP_404_NOT_FOUND)

        except:
            message = {"feedbackResponse": "something went wrong when updating user"}
            return Response(message, status = status.HTTP_500_INTERNAL_SERVER_ERROR)


####################################    DELETE A USER   ##################################


class DeleteUserView(APIView):
    """View to delete a single user using is id"""

    def delete(self, request):
        """Delete a user"""

        try:
            user_id = int(request.query_params.get("userId"))

            if get_user_model().objects.filter(id = user_id).exists():

                user = get_user_model().objects.get(id = user_id)
                user.delete()

                message = {"feedbackResponse": "User has been deleted successfully"}
                return Response(message, status = status.HTTP_200_OK)
            else:
                message = {"feedbackResponse": "The user does not exists in the database."}
                return Response(message, status = status.HTTP_404_NOT_FOUND)

        except:
            message = {"feedbackResponse": "something went wrong when retrieving jobs"}
            return Response(message, status = status.HTTP_500_INTERNAL_SERVER_ERROR)



####################################    DELETE ALL USER   ##################################


class DeleteAllUserView(APIView):
    """View to delete all user using is id"""

    def delete(self, request):
        """Delete all users"""

        print("JULES ON CHECK LA DELETION ALL")

        try:
            users = get_user_model().objects.all()
            users.delete()

            empty_users_set = get_user_model().objects.all()
            serializer = UserSerializer(empty_users_set, many = True)

            message = {
                "feedbackResponse": "Users have been deleted successfully",
                "dataResponse": serializer.data
            }
            return Response(message, status = status.HTTP_200_OK)

        except:
            message = {"feedbackResponse": "something went wrong when deleting all users"}
            return Response(message, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
