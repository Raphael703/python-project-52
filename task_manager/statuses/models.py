from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    name = models.CharField(_('name'), max_length=256, unique=True)
    created_at = models.DateTimeField(
        _('created datetime'), default=timezone.now
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Status')
        verbose_name_plural = _('Statuses')
