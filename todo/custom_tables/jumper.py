from ..table import Table

class Jumper(Table):

    def __init__(self):

        self.fields = [
            'id integer PRIMARY KEY AUTOINCREMENT',
            'hash text',
            'url text',
            'page int',
            'position text',
            'constraint unique_hash_jump unique (hash, page, position)',
            'constraint unique_url_jump unique (url, page, position)',
        ]

        super().__init__(name='jumper', fields=self.fields, dname='jumper') 
