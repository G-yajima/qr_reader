
class QrRecorder():
    def __init__(self):
        self._recods = set()
    
    @property
    def recods(self):
        return list(self._recods)
    
    def add_decodes(self, qr_list):
        self._recods.update(qr_list)