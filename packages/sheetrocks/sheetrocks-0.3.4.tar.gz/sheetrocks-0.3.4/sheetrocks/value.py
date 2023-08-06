from enum import Enum
from datetime import datetime
from typing import Any, Type, TypeVar, Generic

class ValueType(Enum):
    EMPTY = 0
    NUMBER = 1
    DATE = 2
    BOOLEAN = 3
    TEXT = 4
    ARRAY = 5

T = TypeVar('T')

class Value(Generic[T]):
    def __init__(self, valueType : ValueType, number : float, text : str, date : datetime, boolean : bool, array : list[list[T]]):
        self.valueType = valueType
        self.number = number

        if isinstance(self.number, int):
            self.number = float(self.number)
        self.text = text
        self.date = date
        self.boolean = boolean
        self.array = array
    def get(self) -> Any:
        if self.valueType == ValueType.EMPTY:
            return None
        if self.valueType == ValueType.NUMBER:
            return self.number
        if self.valueType == ValueType.DATE:
            return self.date
        if self.valueType == ValueType.BOOLEAN:
            return self.boolean
        if self.valueType == ValueType.TEXT:
            return self.text
        if self.valueType == ValueType.ARRAY:
            result = []
            if self.array is not None and len(self.array) > 0:
                for row in self.array:
                    resultRow = []
                    if row is not None and len(row) > 0:
                        for cell in row:
                            resultRow.append(cell.get())
                    result.append(resultRow)
            return result
    @classmethod
    def fromvar(cls, var : Any):
        valueType = None
        number = None
        text = None
        date = None
        boolean = None
        array = None

        if var is None:
            valueType = ValueType.EMPTY
        if isinstance(var, float):
            valueType = ValueType.NUMBER
            number = var
        if isinstance(var, int):
            valueType = ValueType.NUMBER
            number = float(var)
        if isinstance(var, str):
            valueType = ValueType.TEXT
            text = var
        if isinstance(var, datetime):
            valueType = ValueType.DATE
            date = var
        if isinstance(var, bool):
            valueType = ValueType.BOOLEAN
            boolean = var
        if isinstance(var, list):
            valueType = ValueType.ARRAY
            array = []
            if var is not None and len(var) > 0:
                for row in var:
                    newRow = []
                    if row is not None and len(row) > 0:
                        for cell in row:
                            newRow.append(Value.fromvar(cell))
                    array.append(newRow)
        return cls(valueType, number, text, date, boolean, array)