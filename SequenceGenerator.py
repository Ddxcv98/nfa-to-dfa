class SequenceGenerator:
    def __init__(self):
        self.n = 1
        self.o = 65

    def next_string(self):
        string = ''
        c = chr(self.o)

        for i in range(self.n):
            string += c

        if self.o == 90:
            self.o = 65
            self.n += 1
        else:
            self.o += 1

        return string
