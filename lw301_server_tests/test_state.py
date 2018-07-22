# coding: utf-8
import datetime
from unittest import TestCase

from lw301_server_app import state


class TestState(TestCase):

    def test_update_state(self):
        s = state.State()
        self.assertEqual(len(s.temperature_history), 0)
        self.assertIsNone(s.last_mac)
        now = datetime.datetime.utcnow()
        value = state.Temperature(mac='00001234abcd', channel='1', celsius=28.5)
        s.update_history('temperature', value)
        self.assertEqual(s.last_mac, '00001234abcd')
        self.assertEqual(len(s.temperature_history), 1)
        self.assertEqual(s.temperature_history[0][1], value)
        self.assertGreaterEqual(s.temperature_history[0][0], now)

    def test_limit(self):
        s = state.State(history_limit=10)
        for i in range(1, 10 + 1):
            s.update_history('temperature', state.Temperature(mac='00001234abcd', channel=str(i), celsius=28.5))
        self.assertEqual(len(s.temperature_history), 10)
        s.update_history('temperature', state.Temperature(mac='00001234abcd', channel='11', celsius=28.5))
        self.assertEqual(len(s.temperature_history), 10)
        self.assertEqual([x[1].channel for x in s.temperature_history], [str(x) for x in range(2, 11 + 1)])
