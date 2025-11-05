
class QrRecorder():
    def __init__(self):
        self._recodes = set()
    
    @property
    def recodes(self):
        return list(self._recodes)
    
    def add_decodes(self, qr_list):
        self._recodes.update(qr_list)