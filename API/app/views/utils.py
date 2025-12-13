
# utils functions
from django.http import JsonResponse

def check_user_connected(request):
    if request.user.is_authenticated:
        return JsonResponse({'connected': True, 'username': request.user.username})
    else:
        return JsonResponse({'connected': False})

def get_user_details(request):
    if request.user.is_authenticated:
        user = request.user
        user_details = {
            'username': user.username,
            'email': user.email,
        }
        return JsonResponse({'user_details': user_details})
    else:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
        
