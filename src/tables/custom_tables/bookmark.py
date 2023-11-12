from ..table import Table

class Bookmark(Table):

    def __init__(self): 

        self.fields = [
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
        super().__init__(
                name='bookmark', 
                fields=self.fields, 
                dname='bookmark')
