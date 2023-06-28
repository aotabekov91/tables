import os
import hashlib
from ..table import Table

class Cite(Table):
    def __init__(self, loc='/home/adam/code/tables/dparts.db'):
        self.fields=[
            'id integer PRIMARY KEY AUTOINCREMENT', 
            'citing_bibkey text',
            'citing_hash text',
            'cited_bibkey text',
            'cited_hash text',
            'foreign key(citing_hash) references metadata(hash)',
            'foreign key(cited_hash) references metadata(hash)',
            ]
        super().__init__(table='cite', fields=self.fields, loc=loc)
