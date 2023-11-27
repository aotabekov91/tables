from ..table import Table

class Annotation(Table):

    name='annotation'
    dname='annotation'
    uniq={
          'auniq': ('hash', 'kind', 'position', 'function'),
          }
    fields = [
        'id integer PRIMARY KEY AUTOINCREMENT',
        'hash text',
        'text text',
        'content text',
        'position text',
        'function text',
        'kind text not null',
        ]
