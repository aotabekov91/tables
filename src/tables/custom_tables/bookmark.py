from ..table import Table

class Bookmark(Table):

    name='bookmark' 
    dname='bookmark'
    fields = [
        'id integer PRIMARY KEY AUTOINCREMENT',
        'url text',
        'hash text',
        'text text',
        'title text',
        'page integer',
        'keyword text',
        'summary text',
        'position text',
        'kind text not null',
        'constraint unique_doc_bookmark unique (hash, page, position)',
        'constraint unique_web_bookmark unique (url)']
