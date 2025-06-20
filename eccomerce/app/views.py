from django.shortcuts import render
from .models import CustomUser, Category, Product
from rest_framework.viewsets import ModelViewSet
from .serializers import CustomUserSerializer, LoginSerializer, ProductSerializer, CategorySerializer
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .functions import user_login_function

User = get_user_model()

# Create your views here.


class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            response = Response(serializer.data)
        else:
            response = Response(serializer.errors, status=400)

        password = request.data.get('password')

        user = User(**serializer.validated_data)
        user.set_password(password)
        try:
            user.save()
        except Exception as e:
            return Response({"message": "user with that name already exists"}, status=status.HTTP_400_BAD_REQUEST)
        # password = request.data.get('password')
        # repeat_password = request.data.get('repeate_password')
        # if password != repeat_password:
        #     return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        # user = serializer.save(**validated_data)
        print(serializer.data)
        return Response({
            'user': serializer.data,
            'token': serializer.get_token(user)
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
    #     serializer = LoginSerializer(data=request.data)
    #     if serializer.is_valid():
    #         email = serializer.validated_data['email']
    #         password = serializer.validated_data['password']
    #         print(email, password)
    #         user = authenticate(request, username=email, password=password)

    #         if user is not None:
    #             refresh = RefreshToken.for_user(user)
    #             return Response({
    #                 'refresh': str(refresh),
    #                 'access': str(refresh.access_token),
    #             })
    #         return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = user_login_function(email=email, password=password)

            if user is not None:
                return Response({
                    'user': CustomUserSerializer(user).data,
                    'token': CustomUserSerializer().get_token(user)
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer 

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer