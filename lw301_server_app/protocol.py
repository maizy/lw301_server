# coding: utf-8
import re
from urllib.parse import parse_qs


def _convert_to_float(value):
    if value is None or len(value) != 1 or not re.match(r'[0-9.]+', value[0]):
        return None
    try:
        return float(value[0])
    except:
        return None


def _convert_to_int(value):
    if value is None or len(value) != 1 or not re.match(r'[0-9]+', value[0]):
        return None
    try:
        return int(value[0])
    except:
        return None


def _convert_to_string(value):
    if value is None or len(value) != 1:
        return None
    try:
        return value[0]
    except:
        return None


_SENSOR_VALUES_MAP = {
    'ot': ('temperature_celsius', _convert_to_float),
    'oh': ('humidity_relative', _convert_to_int),
}

_GLOBAL_VALUES_MAP = {
    'baro': ('pressure_hPa', _convert_to_int),
}


class UpdateBody:
    body_type = 'update'

    def __init__(self, query: dict):
        self.query = query
        self.mac = _convert_to_string(query.get('mac'))
        self.channel = _convert_to_int(query.get('ch'))
        self.sensor_values = None
        self.global_values = None

        if 'ch' in query:
            values = {}
            for key, (res_key, converter) in _SENSOR_VALUES_MAP.items():
                if key in query:
                    values[res_key] = converter(query[key])
            self.sensor_values = values
        else:
            values = {}
            for key, (res_key, converter) in _GLOBAL_VALUES_MAP.items():
                if key in query:
                    values[res_key] = converter(query[key])
            self.global_values = values

    def __str__(self):
        return ('UpdateBody<mac={s.mac}, global={s.global_values}, '
                'channel={s.channel}, sensor={s.sensor_values}>').format(s=self)

    def __eq__(self, other):
        return type(other) == type(self) and self.query == other.query


def parse_body(body: bytes, logger=None):
    try:
        qs = parse_qs(body.decode('utf-8'))
    except Exception as e:
        logger.exception("Unable to decode body")
        return None
    return UpdateBody(qs)
