from ..table import Table

class Quickmark(Table):

    def __init__(self): 

        self.fields = [
            'id integer PRIMARY KEY AUTOINCREMENT',
            'url text',
            'hash text',
            'mark text',
            'page integer',
            'position text',
            'kind text not null',
            'constraint unique_doc_quickmark unique (hash, page, url, kind, mark)']
        super().__init__(
                name='quickmark', 
                fields=self.fields, 
                dname='quickmark')
