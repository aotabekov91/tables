import re
from .hash import Hash
from ..table import Table
from .metadata import Metadata
from ..utils import keywords, summarize
from ..utils import getPDFContent, getPDFMetadata, getHash

class Part(Table):

    def __init__(self):

        self.fields=[
                'id integer PRIMARY KEY AUTOINCREMENT',
                'hash text',
                'page int',
                'kind text',
                'text text',
                'summary text',
                'keyword text',
                'x1 real',
                'y1 real',
                'x2 real',
                'y2 real',
                'constraint unique_part unique (hash, page, kind, text, x1, y1, x2, y2)',
                ]

        super().__init__(name='part', fields=self.fields, dname='part')

        self.hash=Hash()
        self.metadata=Metadata()

    def addDocument(self, dhash, path):

        data={'hash': dhash, 'kind':'document'}
        row=self.getRow(data)
        if not row:
            text=getPDFContent(path)

            data['text']=text[:5000]
            data['path']=path
            data['summary']=summarize(data['text'])
            data['keyword']=keywords(data['text'])
            self.writeRow(data)

            data={'hash': dhash}
            for k, v in getPDFMetadata(path).items(): data[k]=v
            self.metadata.writeRow(data, uniqueField='hash')

    def addParts(self, data):

        for kind, d in data.items():
            for ind, rowDic in d.items():
                rowDic['kind']=kind
                if rowDic.get('text'):
                    rowDic['keyword']=keywords(rowDic['text'])
                    rowDic['summary']=summarize(rowDic['text'])
                if kind=='author': self.updateAuthor(rowDic)
                if kind=='title': self.updateTitle(rowDic)
                self.writeRow(rowDic)

    def updateAuthor(self, data):

        criteria={'hash': data['hash']}
        row=self.metadata.getRow(criteria)
        if row and row[0]['author']=='':
            self.metadata.updateRow(criteria, {'author': data['text']})

    def updateTitle(self, data):

        criteria={'hash': data['hash']}
        row=self.metadata.getRow(criteria)
        if row and row[0]['title']=='':
            self.metadata.updateRow(criteria, {'title': data['text']})

    def getTreeDict(self, dhash, get_level=None, get_parent=None, kind='children'):

        def number_point_parent(level): 

            if not '.' in level: return 'root'
            return level.rsplit('.', 1)[0].strip('.')

        def number_point_level(text): return text.split(' ', 1)[0].strip('.')

        if not get_level: get_level=number_point_level
        if not get_parent: get_parent=number_point_parent

        data=self.search(f'hash:{dhash} NOT kind:document')
        if data:

            data=sorted(data, key=lambda x: (x['page'], x['y1']))
            root={'children':[], 
                  'subitem': [],
                  'data':{'text': dhash, 'kind':'root'}}
            elements={'root': root}
            last=root
            for d in data:
                if re.match('^[0-9]*$', d['text']):continue
                element={'data':d, 'children':[], 'subitem':[]}
                if d['kind']=='section':
                    level=get_level(d['text'])
                    parent_level=get_parent(level)
                    if parent_level in elements:
                        parent=elements[parent_level]
                    else:
                        parent=elements['root']
                    parent['children']+=[{level: element}]
                    elements[level]=element
                    last=element
                else:
                    if kind=='children':
                        last['children']+=[{None: element}]
                    elif kind=='subitem':
                        last['subitem']+=[element]
            return elements['root']

    def print_tree(self, root):

        print(root['data']['text'][:20])
        for c in root['children']:
            self.print_tree(c)
