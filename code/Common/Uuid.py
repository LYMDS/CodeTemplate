from uuid import uuid1

class Uuid:
    def get_hex(self):
        self.id = uuid1()
        self.value = self.id.hex
        return self.value