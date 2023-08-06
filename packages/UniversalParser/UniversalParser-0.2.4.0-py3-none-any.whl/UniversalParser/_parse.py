from .manager import ChainManager
from ._ntype import *
import os
from typing import Any, Dict

__all__ = [
    'parse',
    'parse_string',
    'parse_json',
    'parse_dict',
    'parse_yaml'
]

ATTR_PREFIX = '@'
CDATA_KEY = '#text'
REAL_CDATA_KEY = 'text_'

def parse_string(
        xml_data: str
        , attr_prefix: str = ATTR_PREFIX
        , cdata_key: str = CDATA_KEY
        , real_cdata_key: str = REAL_CDATA_KEY
    ) -> ChainManager:
    return ChainManager(
        xml_data
        , attr_prefix = attr_prefix
        , cdata_key = cdata_key
        , real_cdata_key = real_cdata_key
    )

def parse(
        xml_path: str
        , attr_prefix: str = ATTR_PREFIX
        , cdata_key: str = CDATA_KEY
        , real_cdata_key: str = REAL_CDATA_KEY
        , encoding: str = 'utf-8'
    ) -> ChainManager:
    with open(xml_path, 'r', encoding=encoding) as fp:
        xml_data = fp.read()

    return parse_string(
        xml_data
        , attr_prefix = attr_prefix
        , cdata_key = cdata_key
        , real_cdata_key = real_cdata_key
    )

def parse_json(
        json_data: Type_JSON
        , encoding='utf-8'
        , attr_prefix: str = ATTR_PREFIX
        , cdata_key: str = CDATA_KEY
        , real_cdata_key: str = REAL_CDATA_KEY
    ) -> ChainManager:

    if os.path.exists(json_data) and os.path.isfile(json_data):
        with open(json_data, 'r', encoding=encoding) as fp:
            json_data = fp.read()

    return ChainManager(
        ''
        , attr_prefix = attr_prefix
        , cdata_key = cdata_key
        , real_cdata_key = real_cdata_key
        , data_switch = ParserType.JSON
        , universal_data = json_data
    )

def parse_yaml(
        yaml_data: str
        , encoding='utf-8'
        , attr_prefix: str = ATTR_PREFIX
        , cdata_key: str = CDATA_KEY
        , real_cdata_key: str = REAL_CDATA_KEY
    ) -> ChainManager:

    if os.path.exists(yaml_data) and os.path.isfile(yaml_data):
        with open(yaml_data, 'r', encoding=encoding) as fp:
            yaml_data = fp.read()

    return ChainManager(
        ''
        , attr_prefix = attr_prefix
        , cdata_key = cdata_key
        , real_cdata_key = real_cdata_key
        , data_switch = ParserType.YAML
        , universal_data = yaml_data
    )

def parse_dict(
        dict_data: Dict[str, Any]
        , attr_prefix: str = ATTR_PREFIX
        , cdata_key: str = CDATA_KEY
        , real_cdata_key: str = REAL_CDATA_KEY
    ) -> ChainManager:
    return ChainManager(
        ''
        , attr_prefix = attr_prefix
        , cdata_key = cdata_key
        , real_cdata_key = real_cdata_key
        , data_switch = ParserType.DICT
        , universal_data = dict_data
    )
