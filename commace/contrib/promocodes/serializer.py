from rest_framework import serializers
from .models import PromoCode, Redemption

from commace.contrib.cart.models import Cart

class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = '__all__'

class RedemptionSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=50, write_only=True)
    cart = serializers.IntegerField(write_only=True)
    message = serializers.CharField(max_length=255, read_only=True)

    def create(self, validated_data):
        data = validated_data
        try:
            cart = Cart.objects.select_related('user').get(id=data['cart'])
            user = cart.user
            promocode = PromoCode.objects.get(code=data['code'], is_active=True, published=True)
            if promocode is not None:
                redemptions = Redemption.objects.select_related('user', 'promocode').filter(promocode=promocode)
                
                if redemptions is not None and \
                    promocode.per_user > 0 and \
                    promocode.number < redemptions.count():
                    user_redemptions_count = Redemption.objects.select_related('user', 'promocode') \
                                        .filter(user=user, promocode=promocode).count()
                    if user_redemptions_count <= promocode.per_user:
                        redemption = Redemption.objects.create(
                            user=user,
                            promocode=promocode
                        )

                        if redemption.id:
                            cart.promocode = promocode
                            cart.save()

                        return redemption
                    else:
                        return {
                            'message': 'Promo Code already redeemed.'
                        }
                else:
                    redemption = Redemption.objects.create(
                        user=user,
                        promocode=promocode
                    )
                    if redemption.id:
                        cart.promocode = redemption
                        cart.save()

                    return redemption
        except PromoCode.DoesNotExist:
            return {
                'code': 404,
                'message': 'Promo Code not found'
            }

    class Meta:
        model = Redemption
        fields = '__all__'
