from django.apps import AppConfig
from django.conf import settings


class Powerdns(AppConfig):

    name = 'powerdns'
    verbose_name = 'PowerDNS'

    def ready(self):
        import autocomplete_light.shortcuts as al
        from powerdns.models.powerdns import Domain, Record
        from django.contrib.auth import get_user_model

        class AutocompleteAuthItems(al.AutocompleteGenericBase):
            choices = (
                Domain.objects.all(),
                Record.objects.all(),
            )
            search_fields = (
                ('name',),
                ('name',)
            )

        al.register(AutocompleteAuthItems)
        # We register the default django User class. If someone wants to use
        # an alternative user model, she needs to register it herself. We can't
        # do it, as we don't know what fields are used there.
        al.register(
            get_user_model(),
            search_fields=getattr(settings, 'POWERDNS_USER_SEARCH_FIELDS',
                                  ['username', 'first_name', 'last_name']),
        )
        al.register(Domain, search_fields=['name'])
        al.register(Record, search_fields=['name', 'content'])
