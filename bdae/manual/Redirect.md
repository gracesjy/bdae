## Redirect
```
import logging
import sys

class StreamToLogger(object):
   """
   Fake file-like stream object that redirects writes to a logger instance.
   """
   def __init__(self, logger, level):
      self.logger = logger
      self.level = level
      self.linebuf = ''

   def write(self, buf):
      for line in buf.rstrip().splitlines():
         self.logger.log(self.level, line.rstrip())

   def flush(self):
      pass
      
def learnMNIST():
   logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
        filename='/tmp/out.log',
        filemode='a'
        )
   
   log = logging.getLogger('foobar')
   sys.stdout = StreamToLogger(log,logging.INFO)
   sys.stderr = StreamToLogger(log,logging.ERROR)
```
