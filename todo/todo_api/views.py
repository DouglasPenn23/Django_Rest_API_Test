from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Todo
from .serializers import TodoSerializer
# Create your views here.

class TodoListApiView(APIView):
    # Create permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        # Filter todo objects by UserID
        todos = Todo.objects.filter(user = request.user.id)
        # Serializes from model object to JSON
        serializer = TodoSerializer(todos, many=True)
        # Return response with serialized data and status as 200_OK
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        # Creates data dictionary w/ User ID added to data. 
        data = {
            'task': request.data.get('task'), 
            'completed': request.data.get('completed'), 
            'user': request.user.id
        }
        # Creates a serialized object
        serializer = TodoSerializer(data=data)
        # Validation Check
        if serializer.is_valid():
            # Save if valid
            serializer.save()
            # Return newly created object
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Return errors if not valid.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)