from enum import Enum


class Choice(Enum):
    ADMIN = 0
    RESIDENT = 1
    VISITOR = 2
    DEFAULT = 'Choose...'
