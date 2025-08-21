from rest_framework import serializers
from .models import CustomUser, Category, Product, Basket, Include
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }
        
    # def create(self, validated_data):
    #     validated_data.pop('repeate_password')  # Remove repeat_password before creating user
    #     user = User(
    #         username=validated_data['username'],
    #         email=validated_data['email']
    #     )
    #     user.set_password(validated_data['password'])  # Hash the password
    #     user.save()
    #     return user

    def get_token(self, user):
        token = RefreshToken.for_user(user)
        return {
            'refresh': str(token),
            'access': str(token.access_token),
        }

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class IncludeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Include
        fields = ['item', 'quantity']

class RelatedProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['slug', 'name', 'image']

    def get_image(self, obj):
        # if obj.image is a list, return the first element
        if isinstance(obj.image, list) and obj.image:
            return obj.image[0]
        return obj.image

class ProductSerializer(serializers.ModelSerializer):
    includes = IncludeSerializer(many=True, read_only=True)
    others = RelatedProductSerializer(source='related_products', many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'category',
            'image', 'stock', 'created_at', 'features', 'slug',
            'new', 'categoryImage', 'includes', 'gallery', 'others'
        ]
        # extra_kwargs = {
        #     'image': {'required': False},
        # }
    
    # def create(self, validated_data):
    #     return User.objects.create(**validated_data)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class BasketSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, queryset=Product.objects.all())

    class Meta:
        model = Basket
        fields = ['products']
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        products = validated_data.pop('products')
        basket, _ = Basket.objects.get_or_create(user=user)
        basket.products.add(*products)
        return basket

        


    