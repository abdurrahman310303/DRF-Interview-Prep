from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import login, logout
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer
from .models import User

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.save()

        login(request, user)

        return Response({
            'message': 'User registered successfully',
            'user': UserSerializer(user).data
        }, status = status.HTTP_201_CREATED)


class UserLoginView(generics.CreateAPIView):

    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data['user']
        
        login(request, user)

        return Response({
            'message': 'Login successful',
            'user': UserSerializer(user).data
        })

class UserLogoutView(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({'message': 'Logout successful'})


class UserProfileView(generics.RetrieveUpdateAPIView):

    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

        