import datetime as dt

from django.contrib.postgres.search import SearchVector
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404

from core import constants as const
from orders.models import Item, Order


def get_order_or_404(order_id: int) -> Order:
    """Return order or error 404."""
    return get_object_or_404(Order, id=order_id)


def get_orders_with_items() -> list[Order]:
    """Return all orders with menu items."""
    orders = Order.objects.prefetch_related('items')
    return orders


def update_order_status(order_id: int, order_status: str) -> Order:
    """Update order status."""
    order = get_order_or_404(order_id=order_id)
    order.status = order_status
    order.save()
    return order


def delete_order(order: Order) -> None:
    """Delete order."""
    return order.delete()


def search_orders(search_query: str) -> list[Order]:
    """
    Search orders by table number and status.
    """
    return (Order.objects.annotate(
        search=SearchVector(
            'table_number', 'status'
        )).filter(search=search_query).prefetch_related('items')
    )


def get_sales_revenue(from_period: dt.date, to_period: dt.date) -> int:
    """
    Get revenue from sales of orders.
    """
    sales_revenue = Order.objects.filter(
        Q(status=const.PAID) & Q(created_at__gte=from_period)
        & Q(created_at__lte=to_period)
    ).aggregate(sales=Sum('total_price')).get('sales')

    if not sales_revenue:
        return const.SALES_REVENUE_MIN_VALUE
    return sales_revenue


def get_orders_total_price(item_ids: list[int]):
    """Return aggregated orders total price."""

    total_price = Item.objects.filter(pk__in=item_ids).aggregate(
        total_price=Sum('price')
    )['total_price']
    return total_price
