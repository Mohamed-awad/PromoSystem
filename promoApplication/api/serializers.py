from rest_framework import serializers
from promoApplication.models import Promo, User


class PromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = [
            'id',
            'user',
            'promo_type',
            'promo_code',
            'created_at',
            'start_time',
            'end_time',
            'promo_amount',
            'is_active',
            'description'
        ]
        read_only_fields = ['id', 'created_at']

    def validate_promo_code(self, value):
        """
        check promo code exist before
        """
        qs = Promo.objects.filter(promo_code__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This promo code already exist")
        return value

    def validate_promo_amount(self, value):
        """
        check promo_amount grater than 0
        """
        if value <= 0:
            raise serializers.ValidationError("promo amount should be greater than 0")
        return value

    def validate_user(self, value):
        """
        check current login user is admin or normal user
        """
        user = User.objects.get(username=value)
        if user.is_admin:
            raise serializers.validationError('promo code should be with normal users only, not admins')
        return value


class PromoPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = [
            'id',
            'promo_amount',
        ]


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'username',
            'password',
            'address',
            'mobile_number'
        ]
        read_only_fields = ['id']

    def validate_username(self, value):
        """
        check username exist before
        """
        qs = User.objects.filter(username__iexact=value)  # including instance
        if qs.exists():
            raise serializers.ValidationError("This username already exist")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
