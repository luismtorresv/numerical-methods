from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any

import pandas as pd


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
    table: pd.DataFrame = field(default_factory=pd.DataFrame)

    def set_success_status(self):
        self.status = ResultStatus.SUCCESS

    def has_failed(self) -> bool:
        match self.status:
            case ResultStatus.FAILURE:
                return True
            case ResultStatus.SUCCESS:
                return False
            case _:
                raise ValueError("Not a valid result status.")


@dataclass
class Table:
    x: list[int] = field(default_factory=list)
    f_x: list[float] = field(default_factory=list)
    error: list[float] = field(default_factory=list)

    def add_row(self, x, f_x, error):
        self.x.append(x)
        self.f_x.append(f_x)
        self.error.append(error)

    def as_dataframe(self):
        return pd.DataFrame.from_dict(asdict(self))


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
