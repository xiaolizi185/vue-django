#coding=utf-8

from functools import wraps
from constant import *

def login_required(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        terminal = self.session.get("_terminal_", None)
        
        if terminal:
            return func(self, *args, **kwargs)
        else:
            self.redirect(self.reverse_url('login'))
    return wrapper