from ..table import Table

class Hash(Table):

    name='hash'
    dname='hash'
    fields = [
        'id integer PRIMARY KEY AUTOINCREMENT',
        'hash text',
        'path text unique',
        'kind text']
