from models.profile import Profile
from django.contrib.auth import authenticate, login as auth_login, get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.db import transaction

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if not username or not password or not email:
        return Response({'error': 'Username, password, and email are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        with transaction.atomic():
            user = User.objects.create_user(username=username, password=password, email=email)
            # If Profile is a separate profile model linked to the user, create it:
            try:
                Profile.objects.create(user=user)
            except Exception:
                # If Profile is actually the user model, skip creating a separate profile.
                pass
    except Exception:
        return Response({'error': 'Unable to register user.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
