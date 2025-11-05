
class QrRecorder():
    def __init__(self):
        self._records = set()
    
    @property
    def records(self):
        return list(self._records)
    
    def add_decodes(self, qr_list):
        self._records.update(qr_list)