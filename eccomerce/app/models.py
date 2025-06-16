from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    pass
# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.conf import settings



# class CustomUser(AbstractUser):
#     def __str__(self):
#         return self.email

#     def save(self, *args, **kwargs):
#         if self.pk is None or not self.password.startswith('pbkdf2_sha256$'):
#             self.set_password(self.password)
#         super().save(*args, **kwargs)

#     def tokens(self):
#         refresh = RefreshToken.for_user(self)
#         return {'refresh': str(refresh), 'acsses': str(refresh.access_token)}