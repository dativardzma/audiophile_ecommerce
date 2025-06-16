from django.shortcuts import render
from .models import CustomUser
from rest_framework.viewsets import ModelViewSet
from .serializers import CustomUserSerializer
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status

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
        
        validated_data = serializer.validated_data
        validated_data.pop('repeate_password', None)

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
    