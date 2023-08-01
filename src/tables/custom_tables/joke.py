from ..table import Table

class Joke(Table):

    def __init__(self): 

        self.fields = [
            'id integer PRIMARY KEY AUTOINCREMENT',
            'author text',
            'name text',
            'text text',
            'constraint unique_quote unique (name, text)',
        ]

        super().__init__(name='joke', fields=self.fields, dname='jokes')
