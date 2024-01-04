from rest_framework.authtoken.models import Token
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Users
from django.contrib.auth import authenticate

class UserViewSet(viewsets.ViewSet):
    """
    Users-API for the Users.
    Handles (POST, GET).
    """

    def create(self, request):
        """create-user

        Args:
            request (json): Contains username and password fiels only.

        Returns:
            dict: Success message/Error message
        """
        try:
            if not request.data.get("username") and not request.data.get("password"):
                data = {"error":"Username and password is mandatory"}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            
            
            username = request.data.get("username")
            password = request.data.get("password")

            if Users.objects.filter(username=username).exists():
                data = {"error":"Username already exists. Create a new username."}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

            user = Users.objects.create(username=username)
            user.set_password(password)
            user.save()
            
            data = {"Message": "User created successfully"}
            return Response(data=data, status=status.HTTP_200_OK)
        
        except Exception as e:
            data = {"Error": str(e)}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request):
        """get-token

        Args:
            request (json): Login credentials ie correct Username and Password.

        Returns:
            dict: Access-Token/Error message
        """
        try:
            if not request.data.get("username") and not request.data.get("password"):
                data = {"error":"Username and password is mandatory"}
                return Response(data=data, status= status.HTTP_400_BAD_REQUEST)

            username = request.data.get("username")
            password = request.data.get("password")

            user = authenticate(request, username=username, password=password, is_active=True)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                data = {"Message":{
                    "token":token.key,
                    "username":username
                }}
                return Response(data=data, status= status.HTTP_200_OK)
            
            else:
                data =  {"error": "Fill the correct password and username"}
                return Response(data=data, status= status.HTTP_401_UNAUTHORIZED)
            
        except Exception as e:
            data = {"Error": str(e)}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            