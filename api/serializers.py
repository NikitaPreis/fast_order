from rest_framework import serializers
from rest_framework.validators import ValidationError

from core import constants as const
from orders.models import Item, Order
from orders.validators import validate_period_of_dates
from services import orders as order_service


class ItemInOrderSerializer(serializers.Serializer):
    """Serializer for item in order."""
    item = serializers.CharField()
    amount = serializers.IntegerField()


class OrderReadSerializer(serializers.ModelSerializer):
    """Serializer for reading the order."""
    items = serializers.StringRelatedField(
        read_only=True,
        many=True
    )

    class Meta:
        model = Order
        fields = ('id', 'table_number', 'items', 'status', 'total_price')


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating the order."""
    status = serializers.CharField(default=const.PENDING)
    items = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Item.objects.all(),
        required=False
    )

    class Meta:
        model = Order
        fields = ('id', 'table_number', 'items', 'status')
        read_only_fields = ('id',)

    def create(self, validated_data):
        """Create order with specified items and calculated total price."""
        items = validated_data.pop('items')
        item_ids = [item.pk for item in items]
        total_price = order_service.get_orders_total_price(item_ids=item_ids)
        table_number = validated_data['table_number']
        order = Order.objects.create(
            table_number=table_number,
            total_price=total_price,
        )
        order.items.set(items)
        return order

    def to_representation(self, instance):
        serializer = OrderReadSerializer(instance)
        return serializer.data


class OrderUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating order status."""

    class Meta:
        model = Order
        fields = ('id', 'table_number', 'items', 'status')
        read_only_fields = ('id', 'table_number', 'items',)

    def validate_status(self, value: str):
        """Check that status is in the list of expected statuses."""
        if value not in const.STATUSES:
            raise ValidationError('Unexpected status')
        return value

    def to_representation(self, instance):
        serializer = OrderReadSerializer(instance)
        return serializer.data


class SalesRevenueSerializer(serializers.Serializer):
    """Serializer for order sales revenue."""

    from_date = serializers.DateField(input_formats=['%Y-%m-%d'])
    to_date = serializers.DateField(input_formats=['%Y-%m-%d'])
    sales_revenue = serializers.SerializerMethodField()

    def validate(self, data):
        """Validate received dates."""
        validate_period_of_dates(
            from_date=data['from_date'], to_date=data['to_date']
        )
        return data

    def get_sales_revenue(self, instance):
        """Get sales revenue field."""
        return order_service.get_sales_revenue(
            from_period=instance['from_date'],
            to_period=instance['to_date']
        )
