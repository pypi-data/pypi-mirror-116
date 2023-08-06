import datetime
from typing import List
from decimal import Decimal

from essencia.models.abstract import Model, Profile
from essencia.descriptors.base import Field, ORM, ListEnumField, AllowRevisit
from essencia.enum.string import EnumStr
from essencia.enum.integer import EnumInt
from essencia.functions import cpf_format


class Client(Model):
    fullname: str = Field(str)
    contact: str = Field(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fullname = kwargs.get("fullname") or kwargs.get("name")
        self.contact = kwargs.get("email") or kwargs.get("phone") or kwargs.get("contact")

    def __str__(self):
        return f"{self.fullname}{f' ({self.contact})' if self.contact else ''}"



class Patient(Profile):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


