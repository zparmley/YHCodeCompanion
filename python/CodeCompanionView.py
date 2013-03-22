import json

class CodeCompanionView(object):
    def __init__(self):
        self.rgb = [0,0,0]
        self.screen = ['', '']
        self.id = 0
        self.appstate = 0

    

    @property
    def json(self):
        return json.dumps({'rgb': self.rgb, 'screen': [str(self.screen[0]).ljust(16, ' '), str(self.screen[1]).ljust(16, ' ')], 'id': self.id, 'appstate': self.appstate})