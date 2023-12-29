from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    name = models.CharField(_('name'), max_length=128, unique=True)
    created_at = models.DateTimeField(
        _('created datetime'), default=timezone.now
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Label')
        verbose_name_plural = _('Labels')
