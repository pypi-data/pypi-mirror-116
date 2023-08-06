from typing import TypeVar, Union

class TextType:
    STR = 0
    INT = 1
    FLOAT = 2
    DECIMAL = 3

class ParserType:
    XML = 0
    JSON = 1
    DICT = 2
    YAML = 3

Type_Path = TypeVar('Type_Path')
Type_JSON = Union[Type_Path, str]
