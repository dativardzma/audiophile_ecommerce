from django.contrib.auth.hashers import check_password
from .models import CustomUser

def user_login_function(email=None, password=None):
    try:
        user = CustomUser.objects.get(email=email)
        if not user.is_active:
            return None
    except CustomUser.DoesNotExist:
        return None

    if check_password(password, user.password):
        return user
    return None
