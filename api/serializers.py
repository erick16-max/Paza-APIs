from rest_framework import serializers
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


from paza.models import Forum, Leader, Resident, Posts, Resident,Comment

User = get_user_model()



# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ("first_name", "last_name", "email", "password")


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    def validate_email(self, value):
        lower_email = value.lower()
        if User.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError("Email already exists")
        return lower_email
    
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','county','association','password']
        # extra_kwargs = {'password':{'write-only':True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['admin'] = user.admin
        

        return token


class LeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leader
        fields = ("first_name", "last_name", "county", "password","neighbourhood_associattion","username")


class ResidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resident
        fields = ("first_name", "last_name", "county", "password","neighbourhood_associattion","username")


class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ('image_name','image_caption','created','image','author', 'likes')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('body','created','post','author',)


class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = ('tittle','description','date_created','topic','name')

        






    

    















