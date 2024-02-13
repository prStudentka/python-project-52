from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False, verbose_name=_('Name'))
    created_at = models.DateTimeField(auto_now_add=True)
	
    class Meta:
        verbose_name = _('Status')
        verbose_name_plural = _('Statuses')