from ..models.profile import Profile
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login as auth_login

@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if not username or not password or not email:
        return Response({'error': 'Username, password, and email are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password, email=email)
    Profile.objects.create(user=user)

    return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request):
    #check if usernameOrEmail contains '@' (email)
    usernameOrEmail = request.data.get('usernameOrEmail')
    if '@' in usernameOrEmail:
        try:
            user_obj = User.objects.get(email=usernameOrEmail)
            username = user_obj.username
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        #if it's username
        username = usernameOrEmail
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        auth_login(request, user)
        return Response({'message': 'Login successful.'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
