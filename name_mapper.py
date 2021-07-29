class NameMapper:
    def __init__(self):
        self.map = {}

    def get_name(self, key):
        if key not in self.map:
            length = len(self.map)
            self.map[key] = chr(length % 26 + 65) * (length // 26 + 1)

        return self.map[key]
