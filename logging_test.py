__author__ = 'Eric'

import logging

LOG_FILENAME = 'logging.txt'
logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.DEBUG,
                    )

logging.debug('log message in the file')

f = open(LOG_FILENAME, 'rt')

try:
    body = f.read()
finally:
    f.close()

print 'File: \n', body