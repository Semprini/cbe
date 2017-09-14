from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete
from django.conf import settings

class AccountsReceivableConfig(AppConfig):
    name = 'cbe.accounts_receivable'

    def ready(self):
        import cbe.signals
        from cbe.accounts_receivable.models import CustomerPayment
        from cbe.accounts_receivable.serializers import CustomerPaymentSerializer

        exchange_prefix = settings.MQ_FRAMEWORK['EXCHANGE_PREFIX'] + self.name
        exchange_header_list = ('vendor','channel')
        
        post_save.connect(  cbe.signals.notify_extra_args(   serializer=CustomerPaymentSerializer, 
                                                                exchange_prefix=exchange_prefix + ".CustomerPayment", 
                                                                exchange_header_list=exchange_header_list)(cbe.signals.notify_save_instance), 
                            sender=CustomerPayment, weak=False)

