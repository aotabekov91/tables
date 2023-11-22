import sqlite3
from os import path, mkdir, popen

class Table:

    def __init__(
            self, 
            fields, 
            loc=None, 
            name=None, 
            idField='id', 
            dname='table',
            folder='~/.tables'
            ):

        self.loc=loc
        self.name=name
        self.dname=dname
        self.fields=fields
        self.idField=idField
        self.folder=path.expanduser(
                folder)
        self.setName()
        self.setLoc()
        self.setFields()
        self.createTable() 

    def setName(self):

        if not self.name: 
            self.name=self.__class__.__name__
        if not self.dname: 
            self.dname=self.name

    def setLoc(self):

        if not self.loc:
            if not path.exists(self.folder): 
                mkdir(self.folder)
            d, f =self.dname, self.folder
            self.loc=f'{f}/{d}.db'
        if not path.exists(self.loc):
            popen(f'sqlite3 {self.loc}')

    def setFields(self):

        exc=['constraint', 'foreign']
        cfields=[]
        for f in self.fields:
            fname=f.split(' ')[0]
            if not fname in exc:
                cfields+=[f.split(' ')]
        self.fdict={}
        for f in cfields:
            self.fdict[f[0]]=f[1]
        cfields=list(self.fdict.keys())
        self.cfields=cfields

    def createTable(self):

        flds=','.join(self.fields)
        sql="CREATE TABLE IF NOT EXISTS {} ({})"
        sql= sql.format(self.name, flds) 
        self.exec(sql)

    def updateRow(
            self, 
            criteria, 
            updateDict
            ):

        upd=[]
        sql='update {} set {} where {}'
        for k, v in updateDict.items():
            v=str(v).replace('"',  '\'')
            upd+=['{} = "{}"'.format(k, v)]
        sql=sql.format(
                self.name, 
                ', '.join(upd),
                self.getCond(criteria))
        self.exec(sql)

    def writeRow(
            self, 
            rowDic=None, 
            update=True, 
            uniqueField=None
            ):

        f=[]
        for k in rowDic.keys():
            if k in self.cfields:
                f+=['"{}"'.format(k)]
        v=[]
        for j, k in rowDic.items(): 
            if j in self.cfields:
                k=str(k).replace('"', '\'')
                v+=['"{}"'.format(k)]
        sql = 'insert into {} ({}) values ({})'
        sql = sql.format(
                self.name, 
                ','.join(f), 
                ','.join(v))
        try:
            cur=self.exec(sql, query=True)
            return cur.lastrowid
        except sqlite3.IntegrityError:
            rows=self.getRow(rowDic)
            if update and rows:
                d=rows[0]
                if not uniqueField: 
                    uniqueField=self.idField
                cp=rowDic.copy()
                c={uniqueField:d[uniqueField]}
                idx=cp.pop(uniqueField, None)
                self.updateRow(c, cp)
                return idx

    def removeRow(
            self, 
            criteria
            ):

        c=self.getCond(criteria)
        sql = 'delete from {} where {}'
        sql = sql.format(self.name, c)
        self.exec(sql)

    def exec(
            self, 
            sql, 
            values=None, 
            query=False
            ):

        def dict_factory(c, r):
            d = {}
            for idx, col in enumerate(c.description):
                d[col[0]] = r[idx]
            return d

        c = sqlite3.connect(self.loc)
        c.row_factory = dict_factory 
        cur=c.cursor()
        try:
            if values:
                cur.execute(sql, values)
                c.commit()
            else:
                cur.execute(sql)
                c.commit()
            if query:
                return cur
            else:
                c.close()
        except:
            pass

    def getCond(self, cond):

        if type(cond)!=list: 
            cond=[cond]
        ctr=[]
        for i in cond:
            for f, v in i.items():
                if type(v)==str and "'" in v: 
                    v=v.replace('"', "'")
                    ctr+=[f'{f}="{v}"']
                else:
                    ctr+=[f"{f}='{v}'"]
        return ' and '.join(ctr)

    def getRow(self, cond):

        cri={}
        for k, v in cond.items():
            if k in self.cfields:
                cri[k]=v
        c=self.getCond(cri)
        sql = 'select * from {} where {}'
        sql = sql.format(self.name, c)
        return self.query(sql)

    def getRows(self):

        sql='select * from {}'
        sql=sql.format(self.name)
        return self.query(sql)

    def query(self, sql):

        r=self.exec(sql, query=True)
        if r: return r.fetchall()
        return []

    def getField(
            self, 
            field, 
            name, 
            value
            ):

        d={'field':name, 'value':value}
        r=self.getRow(d)
        if r and field in r[0].keys(): 
            return r[0][field]

    def setField(
            self, 
            fname, 
            fvalue, 
            name, 
            value
            ):

        d={'field':name, 'value':value}
        self.updateRow(d, {fname:fvalue})
