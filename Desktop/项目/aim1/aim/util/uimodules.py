
from tornado.web import UIModule

class MyUiModule(UIModule):
    def render(self, a, b ):
        return a+b

class Ad(UIModule):
    def render(self, *args, **kwargs):
        return self.render_string('ad.html')
    def css_files(self):
        return 'css/King_Chance_Layer7.css'
    def javascript_files(self):
        return [
            'js/jquery_1_7.js',
            'js/King_Chance_Layer.js',
            'js/King_layer_test.js',
        ]
