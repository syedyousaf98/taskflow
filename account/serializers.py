from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True}}
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
    email = serializers.EmailField(max_length=255, required=True)


class UserChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password1 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        fields = ('current_password', 'password1', 'password2')

    def validate(self, data):
        password1 = data.get('password1')
        password2 = data.get('password2')
        current_password = data.get('current_password')
        user = self.context.get('user')
        if not user.check_password(current_password):
            raise serializers.ValidationError("Current Password doesn't match")
        if password1 != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return data

    def save(self, **kwargs):
        user = self.context.get('user')
        password1 = self.validated_data.get('password1')
        user.set_password(password1)
        user.save()
        self.instance = user
        return self.instance


class UserResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)

    def validate(self, data):
        email = data.get('email')
        is_user_exist = User.objects.filter(email=email).exists()
        if not is_user_exist:
            raise serializers.ValidationError("User doesn't exist")
        return data


class UserResetPasswordConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    re_new_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        new_password = data.get('new_password')
        re_new_password = data.get('re_new_password')
        if new_password != re_new_password:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return data

    def save(self, **kwargs):
        user = self.context.get('user')
        new_password = self.validated_data.get('new_password')
        user.set_password(new_password)
        user.save()
        self.instance = user
        return self.instance