from ..table import Table

class Quote(Table):

    def __init__(self): 

        self.fields = [
            'id integer PRIMARY KEY AUTOINCREMENT',
            'author text',
            'text text',
            'constraint unique_quote unique (author, text)']
        super().__init__(
                name='quote', 
                fields=self.fields, 
                dname='quotes')
