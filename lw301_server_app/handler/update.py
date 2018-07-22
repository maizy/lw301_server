# coding: utf-8

import lw301_server_app.handler
from lw301_server_app import protocol, state


class UpdateHandler(lw301_server_app.handler.Base):

    async def post(self):
        if self.request.body is not None and len(self.request.body) > 0:
            body = protocol.parse_body(self.request.body, self.log)
            if body is not None:
                self.log.debug('Update raw body: {!r}'.format(body))
                await self.process_parsed_body(body)
        # TODO: emulate real server answer
        self.add_header('Content-Type', 'application/json')
        self.write('')

    async def process_parsed_body(self, body):
        app_state = self.application.settings['lw301_state']
        self.log.debug(str(body))

        if body.global_values and 'pressure_hPa' in body.global_values:
            app_state.update_history('pressure', state.Pressure(mac=body.mac, hPa=body.global_values['pressure_hPa']))

        if body.sensor_values and 'temperature_celsius' in body.sensor_values:
            app_state.update_history(
                'temperature',
                 state.Temperature(mac=body.mac, channel=body.channel,
                                   celsius=body.sensor_values['temperature_celsius'])
            )

        if body.sensor_values and 'humidity_relative' in body.sensor_values:
            app_state.update_history(
                'humidity',
                 state.Humidity(mac=body.mac, channel=body.channel,
                                   relative=body.sensor_values['humidity_relative'])
            )
