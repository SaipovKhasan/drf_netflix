from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from movie.models import Genre, Content, Profile, User, WatchedHistory
from movie.validators import toshmat_validator, not_characters
from django.contrib.auth.models import User


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    # contents = ContentSerializer(many=True, read_only=True)

    class Meta:
        model = Genre
        fields = '__all__'


class UserProfileSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30, required=True,
                                     validators=[UniqueValidator(queryset=User.objects.all()),
                                                 toshmat_validator, not_characters])
    first_name = serializers.CharField(max_length=30, allow_blank=True, required=False, validators=[])
    last_name = serializers.CharField(max_length=30, allow_blank=True, required=False)
    email = serializers.EmailField(allow_blank=True, required=False)
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    phone = serializers.CharField(max_length=15, required=True,
                                  validators=[UniqueValidator(queryset=Profile.objects.all())])
    img = serializers.ImageField(allow_empty_file=True, allow_null=True, required=False)

    def validate_username(self, obj):
        print(obj)
        if 'toshmat' in obj:
            raise serializers.ValidationError('Xato')
        return obj

    def validate(self, attrs):
        password = attrs.get('password')
        if password:
            password_confirm = attrs.get('password_confirm')
            if not password_confirm:
                raise serializers.ValidationError({"password_confirm": "Password confirm ni tasdiqlang."})

            if attrs['password'] != attrs['password_confirm']:
                raise serializers.ValidationError('Password va Password confirm bir xil emas.')
        return attrs

    def create(self, validated_data):
        img = validated_data.pop('img', None)
        password = validated_data.pop('password')
        validated_data.pop('password_confirm')
        phone = validated_data.pop('phone')
        with transaction.atomic():
            user = User.objects.create(**validated_data)
            user.set_password(password)
            user.save()
            Profile.objects.create(user=user, phone=phone, img=img)
        return user

    def update(self, instance, validated_data):
        password = validated_data.get('password')
        profile = instance.profile

        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        if password:
            instance.set_password(validated_data['password'])
        instance.save()

        profile.phone = validated_data.get('phone', profile.phone)
        profile.img = validated_data.get('img', profile.img)
        profile.save()

        return instance

    def to_representation(self, instance):
        request = self.context.get('request')

        profile = instance.profile if hasattr(instance, 'profile') else None
        phone = profile.phone if profile else None
        img = profile.img if profile else None
        img_url = img.url if img else None

        full_img_url = request.build_absolute_uri(img_url) if request and img_url else img_url

        return {
            "id": instance.id,
            "username": instance.username,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "email": instance.email,
            "profile": {
                "id": instance.profile.id,
                "phone": phone,
                "img": full_img_url
            }
        }


class ProfileSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=15)

    class Meta:
        model = Profile
        exclude = ('user',)

    def validate_phone(self, obj):
        user = self.context['user']
        profile_exsits = Profile.objects.filter(phone=obj).exclude(user=user).exists()
        if profile_exsits:
            raise serializers.ValidationError("This field must be unique.")
        return obj


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    password = serializers.CharField(max_length=128, write_only=True)
    password_confirm = serializers.CharField(write_only=True, error_messages={
        "required": "Bu maydon kiritilishi zarur"
    })

    class Meta:
        model = User
        exclude = ('groups', 'user_permissions')

    def validate(self, attrs):
        password = attrs.get('password')
        if password:
            password_confirm = attrs.get('password_confirm')
            if not password_confirm:
                raise serializers.ValidationError(
                    {"password_confirm": "password confirmni tasdiqlang."})
            if password != password_confirm:
                raise serializers.ValidationError("`password` va `password_confirm` mos kelmadi.")
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        profile = validated_data.pop('profile')
        validated_data.pop('password_confirm')
        with transaction.atomic():
            user = User.objects.create(**validated_data)
            user.set_password(password)
            user.save()
            Profile.objects.create(user=user, **profile)
        return user

    def update(self, instance, validated_data):
        profile = validated_data.get('profile')
        if profile is not None:
            profile = validated_data.pop('profile')
            instance_profile = instance.profile
            if profile:
                for field, value in profile.items():
                    if hasattr(instance_profile, field):
                        setattr(instance_profile, field, value)
                instance_profile.save()
        print(instance, validated_data)
        for field, value in validated_data.items():
            if 'password' == field:
                instance.set_password(value)
            elif hasattr(instance, field):
                setattr(instance, field, value)
        instance.save()

        return instance


class WatchedHistorySerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    content_name = serializers.StringRelatedField(source='content')

    class Meta:
        model = WatchedHistory
        fields = ('id', 'watched_at', 'user', 'content', 'username', 'content_name', 'is_delete')
        read_only_fields = ('id', 'watched_at')
        extra_kwargs = {
            "user": {"write_only": True},
            "content": {"write_only": True},
        }

    def get_username(self, obj):
        full_name = obj.user.username
        if obj.user.first_name and obj.user.last_name:
            full_name = obj.user.get_full_name()

        return full_name


class UserStatisticsSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    watched_films_count = serializers.IntegerField(read_only=True)
