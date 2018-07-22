# coding: utf-8
from tornado.web import RequestHandler


class Base(RequestHandler):

    def initialize(self):
        self.log = self.application.settings['logger']
