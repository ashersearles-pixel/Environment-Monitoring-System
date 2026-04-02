class Temperature:
    def __init__(self, value, time):
        self.value = value
        self.timestamp = time

    def get_temperature(self):
        return self.value
    
    def get_timestamp(self):
        return self.timestamp