from essencia.models.abstract import Profile
from essencia.descriptors.base import Field


class Assistant(Profile):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

