from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.validators import validate_phone_number

# Create your models here.

class Gateway(models.Model):
    title = models.CharField(_('title'),max_length=50)
    description = models.TextField(_('description'),blank=True)
    avatar = models.ImageField(_('avatar'),upload_to='gateways/',blank=True)
    is_enable = models.BooleanField(_('is enable'),default=True)
    created_time = models.DateTimeField(_('created time'),auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'),auto_now=True)

    class Meta:
        db_table = 'gateways'
        verbose_name = 'Gateway'
        verbose_name_plural = 'Gateways'


class Payment(models.Model):
    STATUS_VOID = 0
    STATUS_PAID = 10
    STATUS_ERROR = 20
    STATUS_CANCELED = 30
    STATUS_REFOUND =31
    STATUS_CHOICES = (
        (STATUS_VOID, _('Void')),
        (STATUS_PAID, _('Paid')),
        (STATUS_ERROR, _('Error')),
        (STATUS_CANCELED, _('Canceled')),
        (STATUS_REFOUND, _('Resolved')),
    )

    STATUS_TRANSLATIONS = {
        STATUS_VOID: _('Payment could not be processed'),
        STATUS_PAID: _('Payment Successful'),
        STATUS_ERROR: _('Payment has encountered an error.'),
        STATUS_CANCELED: _('Payment canceled by the user.'),
        STATUS_REFOUND: _('This payment has been refunded.'),
    }

    user = models.ForeignKey('user.User', related_name='%(class)s', verbose_name=_('user'),on_delete=models.CASCADE)
    package = models.ForeignKey('subscriptions.Package', related_name='%(class)s', verbose_name=_('package'),on_delete=models.CASCADE)
    gateway = models.ForeignKey(Gateway, related_name='%(class)s', verbose_name='gateway', on_delete=models.CASCADE)
    price = models.PositiveIntegerField(_('price'),default=0)
    status = models.PositiveSmallIntegerField(_('status'), choices=STATUS_CHOICES, default=STATUS_VOID, db_index=True)
    device_uuid = models.CharField(_('device uuid'),max_length=40, blank=True)
    token = models.CharField(_('token'),max_length=40, blank=True)

    phone_number = models.CharField(_('phone number'), validators=[validate_phone_number],max_length=20,blank=True, db_index=True)
    consumed_code = models.PositiveIntegerField(_('consumed reference code'),null=True, db_index=True)
    created_time = models.DateTimeField(_('created time'),auto_now_add=True, db_index=True)
    updated_time = models.DateTimeField(_('updated time'),auto_now=True)

    class Meta:
        db_table = 'payments'
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'















