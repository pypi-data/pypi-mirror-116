import datetime
from dataclasses import dataclass
from abc import ABC
from typing import Optional

from essencia.functions import unprivate, make_private, parse_date


class CustomField(ABC):
    def __init__(self, *args, **kwargs):
        self.type = datetime.date if type(self).__name__ in [ "Birthdate" ] else int if type(self).__name__ in ["Phone", "CPF"] else str if len(args) == 0 else args[0]
        self.allow_null = kwargs.pop('allow_null', None)
        self.default = kwargs.pop('default', None)
        self.factory = kwargs.pop('factory', None)
        self.title = kwargs.pop('title', None)
        self.description = kwargs.pop('description', None)


    def __set_name__(self, owner, name):
        self.name = unprivate(name)
        self.private = make_private(name)
        if not self.title:
            self.title = self.name

    def factory_or_default(self, value):
        if value is None:
            if self.factory:
                return self.factory()
            elif self.default:
                return self.default
        return value

    def validate_null(self, value):
        if value is None:
            if not self.allow_null:
                raise ValueError(f'{self.name} cannot be None')

    def setup(self, instance, value):
        return value

    def __set__(self, instance, value):
        value = self.factory_or_default(value)
        self.validate_null(value)
        if value:
            value = self.setup(instance, value)
            assert isinstance(value, self.type)
        setattr(instance, self.private, value)

    def __get__(self, instance, owner):
        return getattr(instance, self.private)


class Fullname(CustomField):
    def setup(self, instance, value):
        if type(value) != str:
            raise ValueError("deve ser uma string")
        if not " " in value:
            raise ValueError("o nome deve ser composto")
        return value.title()


class Birthdate(CustomField):
    def setup(self, instance, value):
        if isinstance(value, datetime.date):
            return value
        elif isinstance(value, (str, tuple, list)):
            return parse_date(value)
        else:
            raise ValueError(f'{type(self)} could not find a birthdate from value {value} of {self.name} attribute.')


class Gender(CustomField):
    def setup(self, instance, value):
        if not value.lower() in [ "m", "masc", "masculino", "male","f", "fem", "feminino" , "female"]:  # todo: gender enum
            raise ValueError("its not a gender")
        return value[0].upper()


class CPF(CustomField):
    def setup(self, instance, value):
        if value is not None:
            value = "".join(filter(str.isdigit, str(value)))
            if len(value) != 11:
                raise ValueError("são necessários 11 dígitos")
            else:
                value = int(value)
        return value


class Phone(CustomField):
    def setup(self, instance, value):
        r = "".join(filter(str.isdigit, str(value)))
        if len(r) < 10 or len(r) > 11:
            raise ValueError("digite um telefone valido com ddd (exemplo: 62...)")
        return int(r)

