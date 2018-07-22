# coding: utf-8
from unittest import TestCase

from lw301_server_app import protocol


class TestBodyParsing(TestCase):

    def test_parse_global_values(self):

        raw = b'mac=00001234abcd&id=c2&pv=0&lb=0&ac=0&reg=0001&lost=0000&baro=982&ptr=0&wfor=0&p=1'
        body = protocol.parse_body(raw)
        self.assertIsNone(body.channel)
        self.assertIsNone(body.sensor_values)
        self.assertEqual(body.global_values, {'pressure_hPa': 982})

    def test_parse_sensor_values(self):
        raw = b'mac=00001234abcd&id=84&rid=12&pwr=0&htr=0&cz=3&oh=77&ttr=0&ot=27.6&ch=1&p=1'
        body = protocol.parse_body(raw)
        self.assertIsNone(body.global_values)
        self.assertEqual(1, body.channel)
        self.assertEqual({'temperature_celsius': 27.6, 'humidity_relative': 77}, body.sensor_values)
