import datetime
from abc import ABC


from essencia.functions import (unprivate, is_dunder, json_parse, cpf_format)
from essencia.descriptors.base import Field

class Model(ABC):
    def __init__(self, *args, **kwargs):
        self._key_ = kwargs.get("key")
        self._meta_ = kwargs.get("meta")
        if not self._key_ and not self._meta_:
            self._model_ = self.__class__.__name__
            self._created_ = kwargs.get('created', datetime.datetime.now().isoformat())
        self._args_ = args
        self._kwargs_ = kwargs

    def __repr__(self):
        return f'{self._model_}({", ".join([ "{}={}".format(k, v) for k, v in self.as_dict().items() if v != None if not is_dunder(k) ])})'

    def as_dict(self):
        return {unprivate(k): v for (k, v) in self.__dict__.items() if not is_dunder(k)}

    def as_json(self):
        return {unprivate(k): json_parse(value=v) for k, v in self.__dict__.items() if not is_dunder(k)}

    def export(self):
        return {
            'meta': {
                'created': self._created_,
                'model': self._model_,
                'str': str(self)
            },
            'data': {
                **self.as_json(),
            }
        }



class Profile(Model):
    fullname = Field(
        str,
        predicate=lambda x: isinstance(x, str) and " " in x,
        transform=lambda x: x.title()
    )
    birthdate = Field(datetime.date, minimum=datetime.date.today().replace(year=1900))
    gender = Field(str, transform=lambda x: "M" if x.lower().startswith("m") else "F")
    cpf = Field(int, transform=lambda x: cpf_format(x), allow_null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fullname = kwargs.get('fullname')
        self.birthdate = kwargs.get('birthdate')
        self.gender = kwargs.get('gender')
        self.cpf = kwargs.get('cpf', None)

    def __str__(self):
        return f'{self.fullname} ({self.birthdate})'
