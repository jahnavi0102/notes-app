from rest_framework.authtoken.models import Token
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Notes
from users.models import Users
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import NotesSerializer



class NotesViewSet(viewsets.ViewSet):
    """
    Notes-API for the authenticated user.
    Handles (POST, GET, PUT, DELETE, SEARCH).
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, pk=None):
        """List

        Args:
            request (json): list all the notes, one note of a user.
            pk (int, optional): pk hence noteId therefore one note else list. Defaults to None.

        Returns:
            dict: Notes data.
        """
        try:
            if pk:
                notes = Notes.objects.filter(users_id=request.user, id=pk)

                if not notes:
                    data = {"error":"Note with this ID doesn't exist"}
                    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
                
                serializer = NotesSerializer(data=notes)
                serializer.is_valid()
                data = {"message":serializer.data}

            else:
                notes = Notes.objects.filter(users_id=request.user.id)
                serializer = NotesSerializer(data=notes, many=True)
                serializer.is_valid()
                data = {"message":serializer.data}

            return Response(data=data, status=status.HTTP_200_OK)
        
        except Exception as e:
            data = {"Error": str(e)}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)



    def create(self, request, pk=None):
        """Create-Share

        Args:
            request (json): Create notes or share with users
            pk (int, optional): ID of notes to be shared with users. Defaults to None.

        Returns:
            dicts: Success message/Error message
        """
        try:
            if pk:
                if not request.data.get("user_id"):
                    data = {"error":"UserId for sharing the notes is mandatory"}
                    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
                
                list_users_id = request.data.get("user_id").split(",")
                print(list_users_id)
                notes = Notes.objects.filter(users_id=request.user.id, id=pk).first()

                if not notes:
                    data = {"error":"Note doesn't exist"}
                    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
                
                
                shared, not_shared = [], []

                for user_id in list_users_id:
                    user = Users.objects.filter(id=user_id).first()
                    if user:
                        notes = Notes(
                            users_id=user.id, 
                            title=notes.title, 
                            description = notes.description
                        )
                        notes.save()
                        shared.append(user.id)

                    else:
                        not_shared.append(user_id)
                        continue

                if len(not_shared) == list_users_id:
                    data = {"Message":"Couldnt share with anyone, no user found."}
                
                else:
                    data = {"Message":f"Shared notes, Unable to share with these ids {not_shared}"}

                return Response(data=data, status=status.HTTP_200_OK)

                
            else:
                if not request.data.get("title") or not request.data.get("description"):
                    data = {"error":"Title and description for the notes is mandatory"}
                    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
                
                notes = Notes(
                    users_id=request.user.id, 
                    title=request.data.get("title"), 
                    description = request.data.get("description")
                    )
        
                notes.save()
                
                data = {"Message": "Notes created successfully"}
                return Response(data=data, status=status.HTTP_200_OK)
            
        except Exception as e:
            data = {"Error": str(e)}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Update

        Args:
            request (json): notes attributes optional
            pk (int): ID of the note to be updated

        Returns:
            dict: Success message/Error message
        """
        try:
            if not request.data.get("title") and not request.data.get("description"):
                    data = {"error":"Title or description for the notes is mandatory to update"}
                    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            
            title, description  = None, None
            
            if request.data.get("title"):
                title = request.data["title"]

            if request.data.get("description"):
                description= request.data["description"]

            notes = Notes.objects.filter(users_id=request.user.id, id=pk).first()
            notes.title = title if title else notes.title
            notes.description = description if description else notes.description
            notes.save()

            data = {"Message": "Notes updated successfully"}
            return Response(data=data, status=status.HTTP_200_OK)
        
        except Exception as e:
            data = {"Error": str(e)}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        
    def destroy(self, request, pk):
        """Delete

        Args:
            request (json): get the user
            pk (int): Id of the notes to be deleted.

        Returns:
            dict:  Success message/Error message
        """
        try:
            notes = Notes.objects.filter(users_id=request.user.id, id=pk)
            notes.delete()
            
            data = {"Message": "Notes deleted successfully"}
            return Response(data=data, status=status.HTTP_200_OK)
        
        except Exception as e:
            data = {"Error": str(e)}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    