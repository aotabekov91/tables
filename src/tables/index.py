import os

from whoosh import query
from whoosh import fields
import whoosh.index as index
from whoosh.fields import Schema 
from whoosh.index import create_in
from whoosh.query import Term, And
from whoosh.qparser import QueryParser

class Index:

    mapping={
            'int':fields.NUMERIC,
            'integer':fields.NUMERIC,
            'real':fields.NUMERIC,
            'text': fields.TEXT,
            'timestamp': fields.TEXT,
             }

    def __init__(self, fields=None, idField='id', name=None, loc=None, ifolder='~/.indexes'):

        self.loc=loc
        self.name=name
        self.idField=idField
        self.ifolder=os.path.expanduser(ifolder)

        self.setName()
        self.create(fields)

    def setName(self):

        if not self.name: self.name=self.__class__.__name__.lower()

    def setLoc(self):

        if self.loc is None:
            if not os.path.exists(self.ifolder): os.mkdir(self.ifolder)
            self.loc=os.path.join(self.ifolder, self.name)
        if os.path.isdir(self.loc):
            self.index=index.open_dir(self.loc, self.name)
        else:
            os.mkdir(os.path.expanduser(self.loc))
            self.index=create_in(self.loc, Schema(**self.fields) , self.name)

    def createFields(self, index_fields):

        data={}
        for f, t in index_fields.items():
            if t in self.mapping:
                data[f]=self.mapping[t]
            else:
                data[f]=self.mapping[t]
            if f==self.idField: data[f]=data[f](stored=True, unique=True)
        return data

    def create(self, fields):

        if fields:
            self.fields=self.createFields(fields)
            self.setLoc()
            self.parser=QueryParser(self.fields, self.index.schema)

    def add(self, row):

        id_term=Term(self.idField, row[self.idField])
        data=self.search(term=id_term, limit=1)
        if not data:
            self.write(row)
        else:
            self.update(row)

    def write(self, data):

        writer = self.index.writer()
        writer.add_document(**data)
        writer.commit()

    def update(self, data):

        writer = self.index.writer()
        writer.update_document(**data)
        writer.commit()

    def delete(self, condDict): 

        query=And([Term(k, v) for k, v in condDict.items()])
        self.index.delete_by_query(query)

    def search(self, query=None, term=None, limit=None, **kwargs):

        self.searcher=self.index.searcher()
        if term:
            return self.searcher.search(term)
        else:
            query = self.parser.parse(query)
            return self.searcher.search(query, limit=limit, **kwargs)
