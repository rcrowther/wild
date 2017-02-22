



class Position:
    def __init__(self, source, line, offset):
        self.source = source
        self.line = line
        self.offset = offset

    def toDisplayString(self, msg = ''):
        return '{0}:{1}: {2}'.format(
            #self.source.pathAsString(),
            self.line,
            self.offset,
            msg
            )

class _NoPosition(Position):
    def __init__(self):
        Position.__init__(self, None, 0, 0)

    def toDisplayString(self, msg = ''):
        return msg

NoPosition = _NoPosition()
