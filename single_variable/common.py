from dataclasses import dataclass
from enum import Enum
from typing import Any


@dataclass
class SingleVariableMethodOutput:
    x_sol: Any
    n_iter: Any
    err: Any


class ResultStatus(Enum):
    SUCCESS = 0
    FAILURE = 1


class ErrorType(Enum):
    ABSOLUTE = 0
    RELATIVE = 1


class ToleranceType(Enum):
    CORRECT_DECIMALS = 0
    SIGNIFICANT_FIGURES = 1


@dataclass
class Result:
    status: ResultStatus = ResultStatus.FAILURE
    error_message: str = ""
    table: Any = None

    def has_failed(self) -> bool:
        match self.status:
            case ResultStatus.FAILURE:
                return True
            case ResultStatus.SUCCESS:
                return False
            case _:
                raise ValueError("Not a valid result status.")


def determine_error_type(tolerance_type):
    match tolerance_type:
        case "Correct Decimals":
            return ErrorType.ABSOLUTE
        case "Significant Figures":
            return ErrorType.RELATIVE
        case _:
            raise ValueError("Not a valid tolerance type.")


def calculate_error(x, x_prev, error_type):
    error = abs(x - x_prev)
    match error_type:
        case ErrorType.ABSOLUTE:
            return error
        case ErrorType.RELATIVE:
            return error / abs(x)
        case _:
            raise ValueError("Not a valid error type.")
