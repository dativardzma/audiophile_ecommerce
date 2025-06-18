from django.contrib.auth.hashers import check_password
from .models import CustomUser

def user_login_function(email=None, password=None):
    """
    Function to authenticate a user with email and password.
    Returns the user object if authentication is successful, otherwise None.
    """
    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return None

    if check_password(password, user.password):
        return user
        print(user)
    return None
