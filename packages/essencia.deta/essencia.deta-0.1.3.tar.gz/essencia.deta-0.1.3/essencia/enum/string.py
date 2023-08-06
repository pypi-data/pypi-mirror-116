__all__=['EnumStr']

from enum import Enum

class BaseStrEnum(str, Enum):
    def __str__(self):
        return self.value

class EnumStr:
    '''String type enumerations'''

    class Val(BaseStrEnum):
        Undefined = "Indefinido"
        Missing = "Ausente"

    class VisitTitle(BaseStrEnum):
        Initial = 'Inicial'
        Regular = 'Regular'
        Revision = 'Revisão'
        Revisit = 'Retorno'
        Session = 'Sessão'
        Undefined = 'Indefinido'

    class Needs(BaseStrEnum):
        MedicalCare = 'Cuidados Médicos'
        Psychotherapy = 'Psicoterapia'
        ExamResult = 'Entrega de Exames'
        Report = 'Relatório Clínico'
        Licence = 'Licença Médica'

    class PaymentMethod(BaseStrEnum):
        Cash = 'Dinheiro'
        Credit = 'Crédito'
        Debit = 'Débito'
        Check = 'Cheque'
        Transfer = 'Transferência'
        Pix = 'Pix'
        Missing = 'Nenhum'

    class MentalItem(BaseStrEnum):
        Mood = 'Humor'
        Affect = 'Afeto'
        Speech = 'Discurso'
        Thought = 'Pensamento'
        Motricity = 'Motricidade'

    class PaymentCharge(BaseStrEnum):
        Full = "100%"
        Half = "50%"
        No = "0%"

    class VisitSite(BaseStrEnum):
        Telemedicine = 'Telemedicina'
        Office = 'Consultório'

    class VisitType(BaseStrEnum):
        First = "Consulta Inicial"
        Regular = "Consulta Regular"
        Revision = "Consulta de Revisão"
        Revisit = "Retorno"
        Session = "Sessão"


