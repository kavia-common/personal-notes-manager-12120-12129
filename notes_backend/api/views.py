from rest_framework import status, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .serializers import RegisterSerializer, LoginSerializer, NoteSerializer
from django.contrib.auth import authenticate, login, logout
from .models import Note
from .permissions import IsOwnerOrReadOnly

@api_view(['GET'])
def health(request):
    return Response({"message": "Server is up!"})

# PUBLIC_INTERFACE
class RegisterView(APIView):
    """
    User registration endpoint.
    POST: Registers a new user.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# PUBLIC_INTERFACE
class LoginView(APIView):
    """
    User login endpoint.
    POST: Authenticates a user and starts a session.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user is not None:
            login(request, user)
            return Response({"message": "Logged in successfully."})
        return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

# PUBLIC_INTERFACE
class LogoutView(APIView):
    """
    User logout endpoint.
    POST: Logs out the currently authenticated user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully."})

# PUBLIC_INTERFACE
class NoteViewSet(viewsets.ModelViewSet):
    """
    Viewset for CRUD operations on Notes.
    """
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
