from ..table import Table

class Quickmark(Table):

    def __init__(self): 

        self.fields = [
            'id integer PRIMARY KEY AUTOINCREMENT',
            'hash text',
            'mark text',
            'position text',
            'constraint unique_doc_quickmark unique (hash, mark)',
        ]

        super().__init__(name='quickmark', fields=self.fields, dname='lura')
