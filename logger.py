#!/usr/bin/env python3

'''

Logger - utility class

'''

import os
from datetime import datetime

# Colors for messages

class MsgColors:
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    ENDC = '\033[0m'


class Logger:

    def __init__(self, path=None, filename=None):
        self.path = path
        self.filename = filename

        if self.path is not None and not os.path.isdir(self.path):
            raise Exception('Invalid path for logfile: %s' % self.path)

        self.file = None
        if self.filename is not None:
            self.file = open(((self.path + '/') if self.path else '') + self.filename, 'w')

    def message(self, severity_str, msg, color_symbol=None):
        result = str(datetime.now().time()) + ' ' + severity_str + ' ' + msg
        if self.file is not None:
            self.file.write(result + '\n')
        else:
            print((color_symbol if color_symbol else '') + result + (MsgColors.ENDC if color_symbol else ''))

    def info(self, msg):
        self.message('[INFO]', msg)

    def warning(self, msg):
        self.message('[WARNING]', msg, MsgColors.WARNING)

    def error(self, msg):
        self.message('[ERROR]', msg, MsgColors.ERROR)

    def close(self):
        if self.file is not None:
            self.file.close()
