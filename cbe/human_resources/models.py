from django.db import models

from cbe.party.models import PartyRole


class Staff(PartyRole):
    def save(self, *args, **kwargs):
        if self.name is None or self.name == "":
            self.name = "Staff"
        super(Staff, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.name,)