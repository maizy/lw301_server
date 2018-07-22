# coding: utf-8
import datetime
from collections import namedtuple

Temperature = namedtuple('Temperature', ['mac', 'channel', 'celsius'])
Humidity = namedtuple('Humidity', ['mac', 'channel', 'relative'])


class Pressure(namedtuple('Pressure', ['mac', 'hPa'])):
    @property
    def mmHg(self):
        return int(self.hPa * 0.7500617)


class State:
    def __init__(self, history_limit=3000):
        self.temperature_history = []
        self.humidity_history = []
        self.pressure_history = []
        self.last_mac = None
        self._history_limit = history_limit

    def update_history(self, measurement, value):
        attr = f'{measurement}_history'
        if not hasattr(self, attr) or type(getattr(self, attr)) != list:
            raise Exception(f'unknown measurement {measurement}')
        current_history = getattr(self, attr)
        if len(current_history) >= self._history_limit:
            current_history = current_history[-(self._history_limit-1):]
        self.last_mac = value.mac
        current_history.append((datetime.datetime.utcnow(), value))
        setattr(self, attr, current_history)
