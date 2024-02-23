from django.db import models
from django.utils.translation import gettext_lazy as _
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from task_manager.users.models import CustomUser


# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False, verbose_name=_('Name'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    status = models.ForeignKey(Status, on_delete=models.PROTECT, null=False, blank=False,
                               related_name='statuses', verbose_name=_('Status'))
    executor = models.ForeignKey(CustomUser, on_delete=models.PROTECT, blank=True, null=True,
                                 default='', related_name='executors', verbose_name=_('Executor'))
    labels = models.ManyToManyField(Label, blank=True, through='RelationModel', through_fields=('task', 'label'),
                                    related_name='labels', verbose_name=_('Labels'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT, blank=False, related_name='author',
                               verbose_name=_('Author'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')


class RelationModel(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
