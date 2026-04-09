class Humidity:
    def __init__(self, value=None, time=None):
        self.value = value
        self.timestamp = time

    def get_value(self):
        return self.value
    def get_timestamp(self):
        return self.timestamp