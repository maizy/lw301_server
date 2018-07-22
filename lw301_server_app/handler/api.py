# coding: utf-8
import lw301_server_app.handler


class _HistoryApiHandler(lw301_server_app.handler.Base):

    measurement = ''

    def convert_value_to_json(self, value):
        return value._asdict()

    def get(self):
        app_state = self.application.settings['lw301_state']
        history = getattr(app_state, '{}_history'.format(self.measurement))

        history_json = []
        for ts, value in reversed(history):
            history_json.append({
                'timestamp': int(ts.timestamp()),
                'utc_datetime': ts.strftime('%Y-%m-%d %H:%M:%S'),
                'value': self.convert_value_to_json(value)
            })

        self.write({
            'measurement': self.measurement,
            'history': history_json
        })


class TemperatureHistoryApiHandler(_HistoryApiHandler):
    measurement = 'temperature'


class PressureHistoryApiHandler(_HistoryApiHandler):
    measurement = 'pressure'

    def convert_value_to_json(self, value):
        res = super().convert_value_to_json(value)
        res['mmHg'] = value.mmHg
        return res

class HumidityHistoryApiHandler(_HistoryApiHandler):
    measurement = 'humidity'
