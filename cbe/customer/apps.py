from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete
from django.conf import settings

class CustomerConfig(AppConfig):
    name = 'cbe.customer'

    def ready(self):
        import cbe.signals
        from cbe.customer.models import Customer, CustomerAccount
        from cbe.customer.serializers import CustomerSerializer,CustomerAccountSerializer

        exchange_prefix = settings.MQ_FRAMEWORK['EXCHANGE_PREFIX'] + self.name
        exchange_header_list = ('managed_by',)
        
        post_save.connect(  cbe.signals.notify_extra_args(   serializer=CustomerSerializer, 
                                                                exchange_prefix=exchange_prefix + ".Customer", 
                                                                exchange_header_list=exchange_header_list)(cbe.signals.notify_save_instance), 
                            sender=Customer, weak=False)

        post_save.connect(  cbe.signals.notify_extra_args(   serializer=CustomerAccountSerializer, 
                                                                exchange_prefix=exchange_prefix + ".CustomerAccount", 
                                                                exchange_header_list=exchange_header_list)(cbe.signals.notify_save_instance), 
                            sender=CustomerAccount, weak=False)
                            