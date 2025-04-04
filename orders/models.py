from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core import constants as const
from core.models import PositionBaseModel


class Category(PositionBaseModel):
    """Menu item category model."""
    class Meta(PositionBaseModel.Meta):
        db_table = 'categories'
        default_related_name = 'category'
        verbose_name = 'Категория меню'
        verbose_name_plural = 'Категории меню'
        default_permissions = (
            'add', 'change', 'delete', 'view'
        )


class Item(PositionBaseModel):
    """Menu item model."""
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория',
        null=False
    )
    price = models.DecimalField(
        max_digits=const.ITEM_PRICE_MAX_DIGITS,
        decimal_places=const.ITEM_PRICE_DECIMIAL_PLACES
    )

    class Meta(PositionBaseModel.Meta):
        db_table = 'items'
        default_related_name = 'item'
        verbose_name = 'Позиция меню'
        verbose_name_plural = 'Позиции меню'
        default_permissions = (
            'add', 'change', 'delete', 'view'
        )

    def __str__(self):
        return f'{self.name}: {self.price} RUB'


class Order(models.Model):
    """Client table order model."""

    class Statuses(models.TextChoices):
        PENDING = const.PENDING, const.PENDING
        READY = const.READY, const.READY
        PAID = const.PAID, const.PAID

    table_number = models.SmallIntegerField(
        verbose_name='Номер стола'
    )

    items = models.ManyToManyField(
        Item,
        through='ItemOrder',
        verbose_name='Список блюд в заказе'
    )

    # The user requests an order much more often than creates or updates it.
    # We store total price in table to calculate value only once.
    total_price = models.DecimalField(
        max_digits=const.ITEM_PRICE_MAX_DIGITS,
        decimal_places=const.ITEM_PRICE_DECIMIAL_PLACES
    )

    status = models.CharField(
        max_length=const.ORDER_STATUS_MAX_LENGTH,
        choices=Statuses.choices,
        default=Statuses.PENDING,
        verbose_name='Статус'
    )

    created_at = models.DateField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        db_table = 'orders'
        default_related_name = 'order'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-id', 'table_number')
        default_permissions = (
            'add', 'change', 'delete', 'view'
        )

    def __str__(self):
        return f'Заказ для столика {self.table_number}. Статус: {self.status}'


class ItemOrder(models.Model):
    """Intermediate model for Item and Order models."""
    item = models.ForeignKey(
        Item,
        on_delete=models.PROTECT,
        verbose_name='Позиция в заказе клиента',
        null=False,
        related_name='order_item'
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='Заказ клиента',
        null=False,
        related_name='order_item'
    )
    amount = models.SmallIntegerField(
        verbose_name='Количество экземпляров позиции в заказе.',
        validators=[
            MinValueValidator(
                const.AMOUNT_OF_ITEMS_IN_ORDER_MIN_VALUE,
                const.AMOUNT_OF_ITEMS_IN_ORDER_ERROR_MESSAGE
            ),
            MaxValueValidator(
                const.AMOUNT_OF_ITEMS_IN_ORDER_MAX_VALUE,
                const.AMOUNT_OF_ITEMS_IN_ORDER_ERROR_MESSAGE
            )
        ],
        default=const.AMOUNT_OF_ITEMS_IN_ORDER_DEFAULT_VALUE,
        null=False
    )

    class Meta:
        db_table = 'order_item'
        default_related_name = 'order_item'
        verbose_name = 'Позиция в заказе'
        verbose_name_plural = 'Позиции в заказе'
        default_permissions = (
            'add', 'change', 'delete', 'view'
        )
