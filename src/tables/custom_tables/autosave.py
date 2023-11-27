from ..table import Table

class Autosave(Table):

    name='autosave'
    dname='autosave'
    uniq={'suniq': ('hash', 'kind')}
    fields = [
        'id integer PRIMARY KEY AUTOINCREMENT',
        'hash text unique',
        'kind text',
        'position text']
