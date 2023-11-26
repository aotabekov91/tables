from ..table import Table

class Tasks(Table):

    name='tasks'
    dname='pomodoro'
    fields = [
    'id integer PRIMARY KEY AUTOINCREMENT',
    'desc text not null',
    'color integer default 0',
    'active integer default 0',
    'task integer' ]

class Pomodoros(Table):

    name='pomodoros'
    dname='pomodoro'
    fields = [
        'id integer PRIMARY KEY AUTOINCREMENT',
        'time timestamp not null',
        'duration integer not null',
        'task integer' ]
