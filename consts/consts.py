from enum import Enum

TIMEOUT_SEC = 5


class Colors(Enum):
    BLACK = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[92m"
    YELLOW = "\033[33m"


class TypeString(Enum):
    CHAR_NUM_UPPER = "char_num_upper"
    CHAR_NUM_LOWER = "char_num_lower"
    CHAR_UPPER = "char_upper"
    CHAR_LOWER = "char_lower"
