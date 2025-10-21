
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
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        return JsonResponse({'user_details': user_details})
    else:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
        
def error_response(message, status=400):
    return JsonResponse({'error': message}, status=status)