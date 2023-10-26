from ..table import Table

class Tasks(Table):

    def __init__(self): 

        self.fields = [
            'id integer PRIMARY KEY AUTOINCREMENT',
            'desc text not null',
            'color integer default 0',
            'active integer default 0',
            'task integer' ]
        super().__init__(
                name='tasks', 
                fields=self.fields, 
                dname='pomodoro')

class Pomodoros(Table):

    def __init__(self): 

        self.fields = [
            'id integer PRIMARY KEY AUTOINCREMENT',
            'time timestamp not null',
            'duration integer not null',
            'task integer' ]
        super().__init__(
                name='pomodoros', 
                fields=self.fields, 
                dname='pomodoro')
