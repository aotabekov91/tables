import os
import zmq

from ..table import Table
from ..utils.utils import getHash

class Hash(Table):

    def __init__(self, parser_port=45231):

        self.fields = [
            'id integer PRIMARY KEY AUTOINCREMENT',
            'hash text',
            'path text unique',
            'kind text',
        ]
        super().__init__(name='hash', fields=self.fields, dname='hash')

        self.dhashes={}
        self.port=parser_port
        self.setConnection()

    def setConnection(self):

        if self.port:
            self.socket=zmq.Context().socket(zmq.PUSH)
            self.socket.connect(f'tcp://localhost:{self.port}')

    def hash(self, path, force_parse=False):

        path=os.path.expanduser(path)
        dhash=getHash(path)
        self.dhashes[path]=dhash

        parse=False
        if not self.getRow({'path':path}):  parse=True

        data={'path':path, 'hash':dhash, 'kind':'document'}
        self.writeRow(data, uniqueField='path')
        if parse or force_parse: self.parse(dhash, path)
        return dhash

    def parse(self, dhash, path):

        data={'kind':'document', 'hash':dhash, 'path':path}
        self.socket.send_json(data)

    def getPath(self, dhash):

        for res in self.getRow({'hash':dhash}):
            if os.path.isfile(res['path']): return res['path']
