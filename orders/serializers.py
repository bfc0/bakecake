from rest_framework.serializers import ModelSerializer, ValidationError
from cakes.models import CustomCake
from orders.models import Order
from django.utils import timezone
INSCRIPTION_PRICE = 500


class CakeSerializer(ModelSerializer):
    class Meta:
        model = CustomCake
        fields = ("price", "title", "level", "shape",
                  "topping", "berry", "decoration")
        read_only_fields = ("price",)

    def create(self, validated_data):
        validated_data["price"] = self.calculate_price(validated_data)
        return super().create(validated_data)

    def calculate_price(self, validated_data):

        total = (validated_data["level"].price +
                 validated_data["shape"].price +
                 validated_data["topping"].price +
                 validated_data["berry"].price +
                 validated_data["decoration"].price
                 )
        if validated_data["title"]:
            total += INSCRIPTION_PRICE
        return total


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ("price", "phone_number", "email",
                  "object_id", "content_object", "content_type", "customer", "address", "comment", "preferred_date", "customer_name")

    def validate_preferred_date(self, value):
        if value < timezone.now():
            raise ValidationError(
                "Preferred date cannot be in the past.")
        return value
