import os


class Logger:

    def __init__(self, path=None, filename=None):
        self.path = path
        self.filename = filename

        if self.path is not None and not os.path.isdir(self.path):
            raise Exception('Invalid path for logfile: %s' % self.path)

        self.file = None
        if self.filename is not None:
            self.file = open(((self.path + '/') if self.path else '') + self.filename, 'w')

    def info(self, msg):
        if self.file is not None:
            self.file.write('[INFO] %s\n' % str(msg))
        else:
            print('[INFO] %s' % str(msg))

    def warning(self, msg):
        if self.file is not None:
            self.file.write('[WARNING] %s\n' % str(msg))
        else:
            print('[WARNING] %s' % str(msg))

    def error(self, msg):
        if self.file is not None:
            self.file.write('[ERROR] %s\n' % str(msg))
        else:
            print('[ERROR] %s' % str(msg))

    def close(self):
        if self.file is not None:
            self.file.close()
