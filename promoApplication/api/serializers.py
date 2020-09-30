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
        qs = Promo.objects.filter(promo_code__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This promo code already exist")
        return value

    def validate_user(self, value):
        user = User.objects.get(username=value)
        if user.is_admin:
            raise serializers.validationError('promo code should be with normal users only, not admins')
        return value
