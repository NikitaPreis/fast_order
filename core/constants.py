SETTINGS_DEBUG = 'True'

NAME_MAX_LENGTH = 256
SLUG_MAX_LENGTH = 256

PENDING = 'в ожидании'
READY = 'готово'
PAID = 'оплачено'
STATUSES = (PENDING, READY, PAID)
ORDER_STATUS_MAX_LENGTH = 50

SALES_REVENUE_MIN_VALUE = .00

ITEM_PRICE_MAX_DIGITS = 15
ITEM_PRICE_DECIMIAL_PLACES = 2

AMOUNT_OF_ITEMS_IN_ORDER_DEFAULT_VALUE = 1
AMOUNT_OF_ITEMS_IN_ORDER_MIN_VALUE = 1
AMOUNT_OF_ITEMS_IN_ORDER_MAX_VALUE = 999
AMOUNT_OF_ITEMS_IN_ORDER_ERROR_MESSAGE = (
    'Убедитесь, что количество позиции в заказе указано верно, '
    'мы не сможем приготовить меньше 1 блюда и больше 999.'
)
DATE_GRATER_THAN_CURRENT_ERROR = 'Дата не может быть больше текущей.'
INVALID_DATE_PERIOD = 'Неверный период даты.'
PAGINATOR_COUNT_PAGES = 10
