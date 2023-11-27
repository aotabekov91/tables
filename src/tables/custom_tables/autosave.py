from ..table import Table

class Autosave(Table):

    name='autosave'
    dname='autosave'
    fields = [
        'id integer PRIMARY KEY AUTOINCREMENT',
        'hash text unique',
        'url text unique',
        'kind text',
        'page int',
        'position text']
