import datetime
from typing import List
from decimal import Decimal

from essencia.models.abstract import Model
from essencia.descriptors.base import Field, ORM, ListEnumField, AllowRevisit
from essencia.enum.string import EnumStr
from essencia.enum.integer import EnumInt


class Appointment(Model):
    provider: str = ORM([ "Doctor", "Therapist" ])
    client: str = ORM([ "Patient", "Client" ])
    needs: List[ EnumStr.Needs ] = ListEnumField(EnumStr.Needs, default=[ EnumStr.Needs.MedicalCare ])
    date: datetime.date = Field(datetime.date, default=datetime.date.today())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.provider = kwargs.get("provider") or kwargs.get("professional")
        self.client = kwargs.get("patient") or kwargs.get("client")
        self.needs = kwargs.get("needs")
        self.date = kwargs.get("date")

    def __str__(self):
        return f'Agendamento de {vars(type(self))[ "client" ]._string_} dia {self.date} com {vars(type(self))[ "provider" ]._string_}'


class Payment(Model):
    method: EnumStr.PaymentMethod = Field(EnumStr.PaymentMethod, default=EnumStr.PaymentMethod.Missing)
    value: Decimal = Field(Decimal, default=Decimal('0'))
    date: datetime.date = Field(datetime.date, factory=datetime.date.today)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.method = kwargs.get("method")
        self.value = kwargs.get("value")
        self.date = kwargs.get("date")

    def __str__(self):
        if self.method == EnumStr.PaymentMethod.Missing:
            return f'Pagamento não realizado'
        return f'R$ {self.value} ({self.method}) pago dia {self.date}'


class Service(Model):
    site = Field(EnumStr.VisitSite)
    title = Field(EnumStr.VisitType)
    provider = ORM([ "Doctor", "Therapist" ])
    value = Field(Decimal)
    allow_revisit = AllowRevisit()
    date = Field(datetime.date, allow_null=True)

    def __init__(self, site, title, provider, value, *args,
                 date=None, allow_revisit=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.site = site
        self.provider = provider
        self.title = title
        self.value = value
        self.date = date
        self.allow_revisit = allow_revisit

    @property
    def max_days(self):
        return 0 if not getattr(self, '_max_days') else getattr(self, '_max_days')

    def __str__(self):
        return "{} {} ( R$ {} )".format(self.title, vars(type(self))[ "provider" ]._string_, str(self.value))


class Invoice(Model):
    appointment: Appointment = Field(Appointment)
    service: Service = Field(Service)
    payment: Payment = Field(Payment)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.appointment = kwargs.get("appointment")
        self.service = kwargs.get("service")
        self.payment = kwargs.get("payment")
        self._balance = self.balance
        self._status = self.status

    @property
    def balance(self):
        return self.payment.value - self.service.value

    @property
    def status(self):
        return EnumInt.PaymentStatus.Finished if self.balance == 0 else EnumInt.PaymentStatus.Debit if self.balance < 0 else EnumInt.PaymentStatus.Credit

    @property
    def delay_days(self):
        if self.balance < 0:
            return (datetime.date.today() - self.appointment.date).days
        return 0


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

