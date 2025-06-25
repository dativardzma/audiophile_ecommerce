from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class CustomUser(AbstractUser):
    pass
# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.conf import settings



# class CustomUser(AbstractUser):
#     def __str__(self):thon m
#         return self.email

#     def save(self, *args, **kwargs):
#         if self.pk is None or not self.password.startswith('pbkdf2_sha256$'):
#             self.set_password(self.password)
#         super().save(*args, **kwargs)

#     def tokens(self):
#         refresh = RefreshToken.for_user(self)
#         return {'refresh': str(refresh), 'acsses': str(refresh.access_token)}

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    features = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
