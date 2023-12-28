from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from task_manager.statuses.models import Status


class Task(models.Model):
    name = models.CharField(_('name'), max_length=256, unique=True)
    description = models.TextField(_('description'), blank=True)
    status = models.OneToOneField(
        Status,
        on_delete=models.PROTECT,
        related_name='task',
        verbose_name=_('status'),
    )
    creator = models.OneToOneField(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name='creator',
        verbose_name=_('creator'),
    )
    executor = models.OneToOneField(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name='executor',
        blank=True,
        null=True,
        verbose_name=_('executor'),
    )
    created_at = models.DateTimeField(
        _('created datetime'), default=timezone.now
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
