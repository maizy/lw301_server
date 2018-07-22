# coding: utf-8
import lw301_server_app.handler


class LoggingHandler(lw301_server_app.handler.Base):

    async def get(self):
        await self.send_stub()

    async def post(self):
        await self.send_stub()

    async def put(self):
        await self.send_stub()

    async def delete(self):
        await self.send_stub()

    async def patch(self):
        await self.send_stub()

    async def head(self):
        await self.send_stub()

    async def options(self):
        await self.send_stub()

    async def send_stub(self):
        self.clear_header('Server')
        self.clear_header('Content-Type')
        self.clear_header('Date')
        self.set_header('Content-Type', 'application/json')
        try:
            body_str = self.request.body.decode('utf-8')
        except:
            body_str = repr(self.request)
        self.log.info('Unknown request\n{req!r}\nHeaders: {h!r}\nBody ({body_len} bytes):\n----\n{body}\n----'
                       .format(req=self.request, h=dict(self.request.headers), body_len=len(self.request.body),
                               body=body_str))
        self.write('')

    def compute_etag(self):
        return None
