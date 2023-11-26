from ..table import Table

class Annotation(Table):

    name='annotation'
    dname='annotation'
    fields = [
        'id integer PRIMARY KEY AUTOINCREMENT',
        'kind text',
        'page int',
        'hash text',
        'url text',
        'text text',
        'content text',
        'position text',
        'function text',
        'constraint unique_document unique (hash, page, position)',
        'constraint unique_web unique (url, position)']
