from ..table import Table

class Part(Table):

    def __init__(self):

        self.fields=[
                'id integer PRIMARY KEY AUTOINCREMENT',
                'hash text',
                'page int',
                'kind text',
                'text text',
                'summary text',
                'keyword text',
                'x1 real',
                'y1 real',
                'x2 real',
                'y2 real',
                'constraint unique_part unique (hash, page, kind, text, x1, y1, x2, y2)']
        super().__init__(
                name='part', 
                fields=self.fields, 
                dname='part')
