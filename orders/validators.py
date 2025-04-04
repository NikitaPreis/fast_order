import datetime as dt

from django.core.exceptions import ValidationError

from core import constants as const


def validate_period_of_dates(
    from_date: dt.date, to_date: dt.date
) -> None:
    """Validate period of dates."""
    current_date = dt.datetime.now().date()

    if from_date > current_date or to_date > current_date:
        raise ValidationError(const.DATE_GRATER_THAN_CURRENT_ERROR)

    if from_date > to_date:
        raise ValidationError(const.INVALID_DATE_PERIOD)
