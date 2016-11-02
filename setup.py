from distutils.core import setup
setup(name='cbe',
      version='1.0',
      py_modules=[
        'cbe.party.models','cbe.party.admin','cbe.party.serializers','cbe.party.views',
        'cbe.location.models','cbe.location.admin','cbe.location.serializers','cbe.location.views',
        'cbe.business_interaction.models','cbe.business_interaction.admin','cbe.business_interaction.views',
        'cbe.urls','cbe.serializer_fields'
        ],
      )