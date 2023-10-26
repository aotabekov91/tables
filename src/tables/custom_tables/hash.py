from ..table import Table

class Hash(Table):

    def __init__(self):

        self.fields = [
            'id integer PRIMARY KEY AUTOINCREMENT',
            'hash text',
            'path text unique',
            'kind text']
        super().__init__(
                name='hash', 
                fields=self.fields, 
                dname='hash')
