from enum import Enum
from datetime import datetime
from typing import Any, TypeVar, Generic

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