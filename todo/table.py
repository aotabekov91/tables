import os
import sqlite3
from sqlite3 import connect, Row, IntegrityError

from .index import Index

class Table:

    def __init__(self, 

                 fields, 
                 idField='id', 
                 name=None, 
                 loc=None, 
                 dname='table',
                 tfolder='~/.tables', 
                 ifolder='~/.indexes'):

        self.loc=loc
        self.name=name
        self.dname=dname
        self.fields=fields
        self.idField=idField

        self.tfolder=os.path.expanduser(tfolder)
        self.ifolder=os.path.expanduser(ifolder)

        self.setName()
        self.setLoc()
        self.setFields()
        self.setIndex()
        self.createTable() 

    def setName(self):

        if not self.name: self.name=self.__class__.__name__
        if not self.dname: self.dname=self.name

    def setIndex(self):

        self.index=Index(self.fields_dict, self.idField, self.name, ifolder=self.ifolder)

    def setLoc(self):

        if not self.loc:
            if not os.path.exists(self.tfolder): os.mkdir(self.tfolder)
            self.loc=f'{self.tfolder}/{self.dname}.db'

        if not os.path.exists(self.loc):
            os.popen(f'sqlite3 {self.loc}')

    def setFields(self):

        exclude=['constraint', 'foreign']
        clean_fields=[f.split(' ') for f in self.fields if not f.split(' ')[0] in exclude]

        self.fields_dict={}
        for f in clean_fields:
            self.fields_dict[f[0]]=f[1]
        self.clean_fields=list(self.fields_dict.keys())

    def cleanFields(self): return self.clean_fields

    def createTable(self):

        sql= "CREATE TABLE IF NOT EXISTS {} ({})".format(
                self.name, ','.join(self.fields))
        self.execute(sql)

    def search(self, *args, **kwargs):

        found=self.index.search(*args, **kwargs)
        data=[]
        for f in found:
            fields=f.fields()
            row=self.getRow({self.index.idField:f[self.index.idField]})
            if row: fields.update(row[0])
            data+=[fields]
        return data

    def indexRows(self, rowDic, kind='add'):

        rows=self.getRow(criteria=rowDic)
        for row in rows:
            if kind=='add':
                self.index.add(row)
            elif kind=='delete':
                self.index.delete({'id': row['id']})

    def updateRow(self, criteria, updateDict):

        condition=self.getConditionDict(criteria)
        sql='update {} set {} where {}'
        updates=['{} = "{}"'.format(
            k, str(v).replace('"', '\'')) for k, v in updateDict.items()]
        update=', '.join(updates)
        sql=sql.format(self.name, update, condition)
        self.execute(sql)
        cr=criteria.copy()
        up=updateDict.copy()
        cr.update(up)
        self.indexRows(cr, kind='add')

    def writeRow(self, rowDic=None, update=True, uniqueField=None):

        f=['"{}"'.format(k) for k in rowDic.keys() if k in self.clean_fields]
        fields=','.join(f)
        v=['"{}"'.format(str(k).replace('"', '\'')) for j, k in rowDic.items() 
           if j in self.clean_fields]
        values=','.join(v)
        sql = f'insert into {self.name} ({fields}) values ({values})'
        try:
            self.execute(sql)
            self.indexRows(rowDic, kind='add')
        except sqlite3.IntegrityError:
            rows=self.getRow(rowDic)
            if update and rows:
                data=rows[0]
                if not uniqueField: uniqueField=self.idField
                criteria={uniqueField:data[uniqueField]}
                copy=rowDic.copy()
                copy.pop(uniqueField, None)
                self.updateRow(criteria, copy)

    def removeRow(self, criteria):

        condition=self.getConditionDict(criteria)
        sql = f'delete from {self.name} where {condition}'
        self.execute(sql)
        self.indexRows(criteria, kind='delete')

    def execute(self, sql, values=None, query=False):

        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d

        con = connect(self.loc)
        con.row_factory = dict_factory 
        cur=con.cursor()

        try:
            if values:
                cur.execute(sql, values)
                con.commit()
            else:
                cur.execute(sql)
                con.commit()
            if query:
                return cur
            else:
                con.close()
        except:
            pass

    def getConditionDict(self, criteria):

        if type(criteria)!=list: criteria=[criteria]
        ctr=[]
        for i in criteria:
            for f, v in i.items():
                if type(v)==str and "'" in v: 
                    v=v.replace('"', "'")
                    ctr+=[f'{f}="{v}"']
                else:
                    ctr+=[f"{f}='{v}'"]
        return ' and '.join(ctr)

    def getRandomRow(self):

        sql=f'SELECT * FROM {self.name} ORDER BY RANDOM() LIMIT 1'
        return self.query(sql)

    def getRow(self, criteria):

        criteria={k:v for k, v in criteria.items() if k in self.clean_fields}
        condition=self.getConditionDict(criteria)
        sql = f'select * from {self.name} where {condition}'
        return self.query(sql)

    def getAll(self):

        return self.query(f'select * from {self.name}')

    def query(self, sql):

        cur=self.execute(sql, query=True)
        if cur: 
            return cur.fetchall()
        else:
            return []

    def getField(self, fieldName, row_id_name, row_id_value):

        found=self.getRow({'field':row_id_name, 'value':row_id_value})
        if len(found)>0 and fieldName in found[0].keys(): return found[0][fieldName]

    def setField(self, fieldName, fieldValue, row_id_name, row_id_value):

        self.updateRow({'field':row_id_name, 'value':row_id_value}, {fieldName:fieldValue})

    def openRow(self, criteria): pass
