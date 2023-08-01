from collections import OrderedDict

class Tables(OrderedDict):

    def __init__(self):

        super().__init__()

    def add_table(self, tableClass, tableName=None): 

        table=tableClass()
        if tableName is None: 
            tableName=table.__class__.__name__.lower().replace('table', '') 
        setattr(self, tableName, table)
