from ..table import Table

class Autosave(Table):

    def __init__(self):

        self.fields = [
            'id integer PRIMARY KEY AUTOINCREMENT',
            'hash text unique',
            'url text unique',
            'kind text',
            'page int',
            'position text']
        super().__init__(
                name='autosave', 
                fields=self.fields, 
                dname='autosave') 
