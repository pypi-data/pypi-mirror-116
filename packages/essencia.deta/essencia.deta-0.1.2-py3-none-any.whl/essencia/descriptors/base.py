import datetime
from abc import ABC
from enum import Enum
from decimal import Decimal

from essencia.enum.string import EnumStr as ES
from essencia.enum.integer import EnumInt as EI
from essencia.enum.tuple import EnumTuple as ET
from essencia.settings import SEPARATOR
from essencia.functions import (unprivate, make_private, parse_date)


class Descriptor(ABC):
    def __init__(self, *args, **kwargs):
        if len(args) >= 1:
            self._type_ = args[ 0 ]
        else:
            self._type_ = None
        self.default = kwargs.pop("default", False)
        self.factory = kwargs.pop("factory", False)
        self.allow_null = kwargs.pop("allow_null", False)
        self.title = kwargs.pop("title", None)
        self.description = kwargs.pop("description", None)
        self.predicate = kwargs.pop("predicate", None)
        self.transform = kwargs.pop("transform", None)

    def __set_name__(self, owner, name):
        self.private = make_private(name)
        self.name = unprivate(name)

    def __get__(self, obj, owner=None):
        return getattr(obj, self.private)

    def setup(self, value):
        if value == 0:
            pass
        elif value == None:
            if self.factory != None:
                value = self.factory()
            elif self.default != None:
                value = self.default
        return value

    def parse(self, obj, value):
        print(f"parsing field {self.name} with object type {type(obj)}")
        return value

    def validate(self, value):
        if value == None:
            if not self.allow_null:
                raise ValueError(f"The field {self.name} cannot be None.")
        if self.predicate:
            if not self.predicate(value):
                raise ValueError(
                    f"o valor de {self.name} ({value}) não pode ser validado por predicado falso ({self.predicate})")
        if self._type_:
            if not isinstance(value, self._type_):
                raise ValueError(f"TypeError: {self.name} expect type {self._type_} but {type(value)} found")

    def __set__(self, obj, value):
        parsed = self.parse(obj, self.setup(value))
        self.validate(value=parsed)
        if self.transform:
            parsed = self.transform(parsed)
        setattr(obj, self.private, parsed)


class IntEnumDescriptor(Descriptor):
    '''Base descriptor class.'''

    def __init__(self, enum, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enum = enum

    def validate(self, value):
        super().validate(value)
        if not type(value) == self.enum:
            if isinstance(value, (list, set)):
                for i in value:
                    if not type(i) == self.enum:
                        raise ValueError(
                            "type of value of {} is {}, dismatch of vtype {}".format(self.name, type(i), self.enum))
            else:
                raise ValueError(
                    "type of value of {} is {}, dismatch of vtype {}".format(self.name, type(value), self.enum))


class IntEnumField(IntEnumDescriptor):
    def parse(self, obj, value):
        if type(value) == int:
            return self.enum(value)
        else:
            return value


class ListEnumField(IntEnumDescriptor):
    def parse(self, obj, value):
        if type(value) == int:
            return [ self.enum(value) ]
        elif isinstance(value, (list or tuple)):
            v = [ ]
            for item in value:
                if type(item) == int:
                    v.append(self.enum(item))
                else:
                    v.append(item)
            value = v
        return value


class Field(Descriptor):
    '''
    Adds choices, options, minimum, maximum, allow_blank and auto_now
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = kwargs.pop("choices", list())
        self.options = kwargs.pop("options", list())
        if len(args) == 0:
            # if there is not arg, it tries to set _type_ if there is choices or options
            if not len(self.choices) > 0 and not len(self.options) > 0:
                self._type_ = None
            else:
                if len(self.choices) > 0:
                    assert isinstance(self.choices, Enum), "choices may use only Enum classes"
                    self._type_ = type(self.choices[ 0 ])
                elif len(self.options) > 0:
                    self._type_ = type(self.options[ 0 ])
        else:
            self._type_ = args[ 0 ]
        self.auto_now = kwargs.pop("auto_now", False)
        if self.auto_now:
            self._type_ = datetime.datetime
            self.factory = datetime.datetime.now
        self.allow_blank = kwargs.pop("allow_blank", False)
        if self.allow_blank:
            self.default = ""
        self.minimum = kwargs.pop("minimum", None)
        self.maximum = kwargs.pop("maximum", None)

    def validate(self, value):
        if not value and value != 0:
            raise ValueError(f'field {self.name}  cannot be None')
        if len(self.options) > 0:
            if not value in self.options:
                raise ValueError(f"{self.name} only accept one of options: {self.options}")
        if self.minimum:
            if isinstance(value, (str, tuple, list)):
                if len(value) < self.minimum:
                    raise ValueError(f"the minimum size for {self.name} is {self.minimum}")
            if isinstance(value, (int, float, Decimal, datetime.date, datetime.datetime, datetime.timedelta)):
                if value < self.minimum:
                    raise ValueError(f"the minimum date for {self.name} is {self.minimum}")
        if self.maximum:
            if isinstance(value, (str, tuple, list)):
                if len(value) > self.maximum:
                    raise ValueError(f"the maximum size for {self.name} is {self.maximum}")
            if isinstance(value, (int, float, Decimal, datetime.date, datetime.datetime, datetime.timedelta)):
                if value > self.maximum:
                    raise ValueError(f"the maximum date for {self.name} is {self.minimum}")
        if self.predicate:
            if not self.predicate(value):
                raise ValueError(f"predicate {self.predicate} False for {self.name} with value {value}")

    def parse(self, obj, value):
        value = self.setup(value)
        print(f"parsin {self.private}")
        if self._type_ != None and value != None:
            if type(value) != self._type_:
                print(f'field "{self.name}" is {self._type_} but value is {type(value)}')
                if self._type_ == Decimal:
                    try:
                        value = self._type_(str(value or 0))
                    except BaseException as e:
                        raise ValueError(e)
                elif issubclass(self._type_, datetime.date):
                    value = parse_date(value)
                elif issubclass(self._type_, int):
                    if isinstance(value, (str, float, Decimal)):
                        value = int(value)
                elif issubclass(self._type_, float):
                    if isinstance(value, (str, int, Decimal)):
                        value = float(value)
                print(f'parsed value of "{self.name}" is {value} of type {type(value)}')
            else:
                print(f"type matched: ({self._type_})")
        return value

    def __set__(self, obj, value):
        value = self.parse(obj, self.setup(value))
        if self.transform and value:
            value = self.transform(value)
        self.validate(value)
        setattr(obj, self.private, value)


class AllowRevisit(Descriptor):

    def __set__(self, obj, value):
        if obj.value == 0:
            setattr(obj, self.private, False)
            setattr(obj, '_charge', ES.PaymentCharge.No)
            setattr(obj, '_max_days', EI.Week.Zero)
        else:
            if obj.title == ES.VisitType.First:
                setattr(obj, self.private, True)
                setattr(obj, '_charge', ES.PaymentCharge.No)
                setattr(obj, '_max_days', EI.Week.Four)
            elif obj.title == ES.VisitType.Regular:
                setattr(obj, self.private, True)
                setattr(obj, '_charge', ES.PaymentCharge.No)
                setattr(obj, '_max_days', EI.Week.Three)
            elif obj.title == ES.VisitType.Revision:
                setattr(obj, self.private, False)
                setattr(obj, '_charge', ES.PaymentCharge.Half)
                setattr(obj, '_max_days', EI.Week.Two)
            elif obj.title == ES.VisitType.Revisit:
                setattr(obj, self.private, False)
                setattr(obj, '_charge', ES.PaymentCharge.No)
                setattr(obj, '_max_days', EI.Week.Zero)
            elif obj.title == ES.VisitType.Session:
                setattr(obj, self.private, False)
                setattr(obj, '_charge', ES.PaymentCharge.Full)
                setattr(obj, '_max_days', EI.Week.Zero)


class ORM(Descriptor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._list_ = [ ]
        self._args_ = args
        if len(self._args_) == 1:
            if type(self._args_[ 0 ]) == str:
                self._list_.append(self._args_[ 0 ])
            elif type(self._args_[ 0 ]) == list:
                self._list_.extend(self._args_[ 0 ])
        print(self._list_)

    @property
    def key(self):
        return self._key_

    def parse(self, obj, value):
        if not value:
            if self.default:
                return self.default
            if self.allow_null:
                return ES.Val.Missing
        return value

    def validate(self, value):
        if not value:
            if not self.allow_null:
                raise ValueError(f"{self.name} cannot be None")

        if not SEPARATOR in value:
            raise ValueError(f"this key is not valid ({value})")

        if len(value.split(SEPARATOR)) != 3:
            raise ValueError(f"this key is not valid ({value})")

        self._model_, self._key_, self._string_ = value.split(SEPARATOR)

        if not self._model_ in self._list_:
            raise ValueError(f"{self.name} options are {self._list_} but model key is {self._model_}")
