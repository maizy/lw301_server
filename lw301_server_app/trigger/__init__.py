# coding: utf-8
from tornado.ioloop import IOLoop
from tornado.options import OptionParser, define


class Trigger:
    def __init__(self, ioloop: IOLoop, app_options: OptionParser):
        self.ioloop = ioloop
        self.app_options = app_options

    async def on_new_data(self, measurement, value):
        pass

    @staticmethod
    def add_options():
        pass
