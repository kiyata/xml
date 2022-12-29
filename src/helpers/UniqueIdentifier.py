class UniqueIdentifier(object):
    counter = 0

    def __init__(self, prefix):
        self.prefix = prefix

    def next(self):
        self.counter = self.counter + 1
        right = '{:03d}'.format(self.counter)
        return '{0}{1}'.format(self.prefix, right)
