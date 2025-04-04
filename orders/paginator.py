from django.core.paginator import Paginator

from core import constants as const


def get_page_obj(queryset, page_number: int):
    """Get page from Paginator."""
    paginator = Paginator(queryset, const.PAGINATOR_COUNT_PAGES)
    page_obj = paginator.get_page(page_number)
    return page_obj
