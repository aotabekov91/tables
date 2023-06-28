from .hash import Hash
from ..table import Table
from ..utils import keywords, summarize, getUrlTitleAndContent

class Bookmark(Table):

    def __init__(self): 

        self.fields = [
            'id integer PRIMARY KEY AUTOINCREMENT',
            'hash text',
            'url text',
            'text text',
            'title text',
            'page integer',
            'keyword text',
            'summary text',
            'position text',
            'kind text not null',
            'constraint unique_doc_bookmark unique (hash, page, position)',
            'constraint unique_web_bookmark unique (url)',
        ]

        super().__init__(name='bookmark', fields=self.fields, dname='bookmark')

        self.hash=Hash()

    def search(self, *args, **kwargs):

        found=super().search(*args, **kwargs)
        for f in found:
            dhash=f.get('hash', None)
            if dhash: f['path']=self.hash.getPath(dhash)
        return found

    def updateRow(self, criteria, updateDict):

        self.updateContent(updateDict)
        super().updateRow(criteria, updateDict)

    def writeRow(self, rowDic, **kwargs):

        rows=self.getRow(rowDic)
        if not rows: self.updateContent(rowDic)
        super().writeRow(rowDic=rowDic, **kwargs)

    def updateContent(self, rowDic):

        if rowDic.get('url', None): rowDic['kind']='url'

        kind=rowDic.get('kind', None)

        if kind=='url':
            title, text, html=getUrlTitleAndContent(rowDic['url'])
            rowDic['text']=text
            if rowDic.get('title', '') in ['', None]: rowDic['title']=title

            if rowDic.get('text', None):
                text=rowDic['text']
                if len(text)>50000: text=text[0:30000]
                rowDic['keyword']=keywords(text)
                rowDic['summary']=summarize(text)
