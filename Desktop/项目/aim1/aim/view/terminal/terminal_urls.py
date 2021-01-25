# coding: utf-8
from tornado.web import url
 
from view.terminal.terminal import *
 
terminal_urls=[
        (r"/websocket", terminado.TermSocket,
             {'term_manager': term_manager}),
        url(r"/terminal/", TerminalPageHandler, name="terminal"),
]