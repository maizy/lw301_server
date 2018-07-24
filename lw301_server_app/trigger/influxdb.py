# coding: utf-8
from logging import getLogger
import time

from tornado.ioloop import IOLoop
from tornado.options import define, OptionParser
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPClientError

from lw301_server_app.trigger import Trigger


class InfluxDbTrigger(Trigger):

    _as_tags = ('mac', 'channel')

    @staticmethod
    def add_options():
        define('influxdb-writeurl', default='http://localhost:8086/write?db=weather', type=str)
        define('influxdb-user', type=str)
        define('influxdb-password', type=str)
        define('influxdb-enabled-measurements', type=str, multiple=True,
               default=['temperature', 'humidity', 'pressure'])

    log = getLogger('influxdb_trigger')

    def __init__(self, ioloop: IOLoop, app_options: OptionParser):
        super().__init__(ioloop, app_options)
        self.http_client = AsyncHTTPClient()

    async def on_new_data(self, measurement, value):
        if measurement not in self.app_options.influxdb_enabled_measurements:
            return

        # delay processing for next ioloop tick
        self.ioloop.add_callback(
            self._send_data,
            value=value,
            measurement=measurement,
            write_url=self.app_options.influxdb_writeurl,
            user=self.app_options.influxdb_user,
            password=self.app_options.influxdb_password,
        )

    def _value(self, value):
        if isinstance(value, int):
            return '{}i'.format(value)
        elif isinstance(value, float):
            return '{:0.2f}'.format(value)
        return '{}'.format(value)

    def _tag_value(self, value):
        if isinstance(value, int):
            value = str(value)
        return self._value(value)

    async def _send_data(self, measurement, value, write_url, user, password, **opts):
        vals = ['{}={}'.format(k.lower(), self._value(v))
                for k, v in value._asdict().items() if k not in self._as_tags]
        if measurement == 'pressure':
            vals.append('mmhg={}'.format(self._value(value.mmHg)))

        tags = ['{}={}'.format(t, self._tag_value(v))
                for t, v in value._asdict().items() if t in self._as_tags]
        tags.insert(0, measurement)

        ts = int(time.time() * (10 ** 9))

        line = '{t} {v} {ts}'.format(t=','.join(tags), v=','.join(vals), ts=ts)

        request = HTTPRequest(url=write_url, method='POST', body=line.encode('utf-8'))
        self.log.debug('send to influxdb: %s', line)
        if user is not None:
            request.auth_mode = 'basic'
            request.auth_username = user
            request.auth_password = password or ''
        try:
            await self.http_client.fetch(request)
        except HTTPClientError as e:
            self.log.error(
                'unable to send data to influxdb.\n'
                'response code=%d, body:\n%s',
                e.code,
                e.response.body
            )
