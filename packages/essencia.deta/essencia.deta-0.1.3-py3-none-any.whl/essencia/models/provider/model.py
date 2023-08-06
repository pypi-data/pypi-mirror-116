from essencia.models.abstract import Profile
from essencia.descriptors.base import Field


class Assistant(Profile):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Provider(Profile):
    profession = Field(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profession = kwargs.get('profession')


class Doctor(Provider):
    profession = Field(str, default="Medicina")
    crm = Field(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.crm = kwargs.get('crm')

    def __str__(self):
        return f'{"Dr." if self.gender.startswith("M") else "Dra."} {self.fullname} ({self.crm})'


class Therapist(Provider):
    licence = Field(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.licence = kwargs.get('licence')

