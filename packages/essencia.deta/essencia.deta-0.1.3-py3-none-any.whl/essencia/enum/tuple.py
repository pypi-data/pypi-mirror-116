__all__=['EnumTuple']

from enum import Enum
from collections import namedtuple

MonthTuple = namedtuple("MonthTuple", "integer usn brn abbr")


class EnumTuple:
    """Tuple type enum"""

    class Month(MonthTuple, Enum):
        JAN = MonthTuple(1, "January", "Janeiro", "Jan")
        FEB = MonthTuple(2, "February", "Fevereiro", "Fev")
        MAR = MonthTuple(3, "March", "Março", "Mar")
        APR = MonthTuple(4, "April", "Abril", "Abr")
        MAY = MonthTuple(5, "May", "Maio", "Mai")
        JUN = MonthTuple(6, "June", "Junho", "Jun")
        JUL = MonthTuple(7, "July", "Julho", "Jul")
        AUG = MonthTuple(8, "August", "Agosto", "Ago")
        SEP = MonthTuple(9, "September", "Setembro", "Set")
        OCT = MonthTuple(10, "October", "Outubro", "Out")
        NOV = MonthTuple(11, "November", "Novembro", "Nov")
        DEZ = MonthTuple(12, "December", "Dezembro", "Dez")

        def __repr__(self):
            return f"<{type(self).__name__}(integer={self.integer}, abbr={self.abbr}, brn={self.brn}, usn={self.usn})>"

        @classmethod
        def members(cls):
            return cls.__members__

        @classmethod
        def int_map(cls):
            return {x.integer: x.brn for x in cls.values()}

        @classmethod
        def values(cls):
            return cls.members().values()

        @classmethod
        def items(cls):
            return cls.members().items()

        @classmethod
        def as_string(cls, v: int):
            return cls.int_map().get(v)


if __name__ == '__main__':
    print(EnumTuple.Month.as_string(12))