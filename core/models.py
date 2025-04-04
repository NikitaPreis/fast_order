from django.db import models

from core import constants as const


class PositionBaseModel(models.Model):
    """Base model with name, slug and description fields."""
    name = models.CharField(
        max_length=const.NAME_MAX_LENGTH,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=const.SLUG_MAX_LENGTH,
        verbose_name='Слаг'
    )
    description = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
