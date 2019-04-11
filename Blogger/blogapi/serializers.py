from rest_framework import serializers
from .models import User, Articles


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'firstname', 'surname', 'email')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')


class ArticleSerializer(serializers.ModelSerializer):
    def get_user(self, obj):
        serializer = UserSerializer(instance=User.objects.get(user=obj.id))
        return serializer.data

    class Meta:
        model = Articles
        fields = ('id', 'title', 'description',
                  'body', 'images', 'slug', 'user')
        read_only_fields = ['slug', 'user', ]
