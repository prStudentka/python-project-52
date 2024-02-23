from django.db.models import DateTimeField, CharField, TextField
from django.db.models import ForeignKey, ManyToManyField, Model, PROTECT, CASCADE
from django.utils.translation import gettext_lazy as _
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from task_manager.users.models import CustomUser


# Create your models here.
class Task(Model):
    name = CharField(max_length=255, unique=True,
                     blank=False, verbose_name=_('Name'))
    description = TextField(blank=True, verbose_name=_('Description'))
    status = ForeignKey(Status,
                        on_delete=PROTECT,
                        null=False,
                        blank=False,
                        related_name='statuses',
                        verbose_name=_('Status'))
    executor = ForeignKey(CustomUser,
                          on_delete=PROTECT,
                          blank=True,
                          null=True,
                          default='',
                          related_name='executors',
                          verbose_name=_('Executor'))
    labels = ManyToManyField(Label,
                             blank=True,
                             through='RelationModel',
                             through_fields=('task', 'label'),
                             related_name='labels',
                             verbose_name=_('Labels'))

    created_at = DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    author = ForeignKey(CustomUser,
                        on_delete=PROTECT,
                        blank=False,
                        related_name='author',
                        verbose_name=_('Author'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')


class RelationModel(Model):
    task = ForeignKey(Task, on_delete=CASCADE)
    label = ForeignKey(Label, on_delete=PROTECT)
