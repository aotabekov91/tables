import os

from whoosh import fields
from whoosh.query import Term

from ..index import Index
from ..utils import keywords, summarize 

# Todo: Should add hash field and update index if hash is changed
# this could be incorporate into the addWiki function

class WikiIndex(Index):

    def __init__(self): 

        self.fields={
                'path': fields.ID(stored=True, unique=True), 
                'title': fields.TEXT(stored=True), 
                'text': fields.TEXT, 
                'change_time': fields.NUMERIC(stored=True),
                'summary': fields.TEXT(stored=True),
                'keyword': fields.KEYWORD(stored=True), 
                }

        super().__init__(fields=self.fields, name='wiki', idField='path')

    def createFields(self, fields):

        return fields

    def addWiki(self, path):

        print('WikiIndex indexing: ', path)

        change_time=os.path.getmtime(path)
        data=self.search(term=Term('path', path), limit=1)

        if not data or data[0]['change_time']<change_time:

            with open(path, 'r') as f: text=' '.join(n.strip('\n') for n in f.readlines())

            p=path.replace('/', ' ').rsplit('.', 1)[0]

            keyword=f'{keywords(text)} {p}'
            summary=summarize(text)
            title=path.rsplit('/', 1)[-1].rsplit('.', 1)[0]

            new_data={'path': path, 
                      'title': title,
                      'text': text, 
                      'change_time': change_time,
                      'keyword': keyword,
                      'summary': summary, 
                      }
            self.add(new_data)
