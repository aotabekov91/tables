from .hash import Hash
from ..table import Table

class Annotation(Table):

    def __init__(self):

        self.fields = [
            'id integer PRIMARY KEY AUTOINCREMENT',
            'kind text',
            'page int',
            'hash text',
            'url text',
            'text text',
            'content text',
            'position text',
            'function text',
            'constraint unique_document unique (hash, page, position)',
            'constraint unique_web unique (url, position)',
        ]

        super().__init__(name='annotation', fields=self.fields, dname='annotation') 

        self.hash=Hash()

    def search(self, *args, **kwargs):

        found=super().search(*args, **kwargs)
        for f in found:
            if f['hash']: f['path']=self.hash.getPath(f['hash'])
        return found
