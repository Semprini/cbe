from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete
from django.conf import settings

class PartyConfig(AppConfig):
    name = 'cbe.party'

    def ready(self):
        import cbe.signals
        from cbe.party.models import Individual, Organisation
        from cbe.party.serializers import IndividualSerializer, OrganisationSerializer

        exchange_prefix = settings.MQ_FRAMEWORK['EXCHANGE_PREFIX'] + self.name
        exchange_header_list_individual = ('marital_status',)
        exchange_header_list_organisation = ('organisation_type',)
        
        post_save.connect(  cbe.signals.notify_extra_args(   serializer=IndividualSerializer, 
                                                                exchange_prefix=exchange_prefix + ".Individual", 
                                                                exchange_header_list=exchange_header_list_individual)(cbe.signals.notify_save_instance), 
                            sender=Individual, weak=False)

        post_save.connect(  cbe.signals.notify_extra_args(   serializer=OrganisationSerializer, 
                                                                exchange_prefix=exchange_prefix + ".Organisation", 
                                                                exchange_header_list=exchange_header_list_organisation)(cbe.signals.notify_save_instance), 
                            sender=Organisation, weak=False)
                            