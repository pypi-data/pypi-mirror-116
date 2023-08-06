import datetime


from essencia.models.abstract import Model
from essencia.descriptors.base import Field, ORM, ListEnumField, AllowRevisit
from essencia.models.business.model import Invoice


class Visit(Model):
    invoice: Invoice = Field(Invoice)
    start = Field(datetime.datetime, factory=datetime.datetime.now)
    duration = Field(datetime.timedelta, allow_null=True)
    notes = Field(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.invoice = kwargs.get('invoice')
        self.start = kwargs.get('start')
        self.duration = kwargs.get('duration')
        self.notes = kwargs.get('notes')

