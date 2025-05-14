## <p>$\bf{\large{\color{#6580DD}LogServer}}$</p>
이것은 로그 서버이다.  Python Module 에 접근을 할 때 작동한다.<br>
그 전에 오류가 나면 이것이 동작하지 않는다. <br>

소스 코드는 다음과 같다. LogServer.py 로 저장한다.<br>
```
import pickle
import logging
import logging.handlers
import socketserver
import struct


class LogRecordStreamHandler(socketserver.StreamRequestHandler):
    """Handler for a streaming logging request.

    This basically logs the record using whatever logging policy is
    configured locally.
    """

    def handle(self):
        """
        Handle multiple requests - each expected to be a 4-byte length,
        followed by the LogRecord in pickle format. Logs the record
        according to whatever policy is configured locally.
        """
        while True:
            chunk = self.connection.recv(4)
            if len(chunk) < 4:
                break
            slen = struct.unpack('>L', chunk)[0]
            chunk = self.connection.recv(slen)
            while len(chunk) < slen:
                chunk = chunk + self.connection.recv(slen - len(chunk))
            obj = self.unPickle(chunk)
            record = logging.makeLogRecord(obj)
            self.handleLogRecord(record)

    def unPickle(self, data):
        return pickle.loads(data)

    def handleLogRecord(self, record):
        # if a name is specified, we use the named logger rather than the one
        # implied by the record.
        if self.server.logname is not None:
            name = self.server.logname
        else:
            name = record.name
        logger = logging.getLogger(name)
        # N.B. EVERY record gets logged. This is because Logger.handle
        # is normally called AFTER logger-level filtering. If you want
        # to do filtering, do it at the client end to save wasting
        # cycles and network bandwidth!
        logger.handle(record)

class LogRecordSocketReceiver(socketserver.ThreadingTCPServer):
    """
    Simple TCP socket-based logging receiver suitable for testing.
    """

    allow_reuse_address = True

    def __init__(self, host='localhost',
                 port=logging.handlers.DEFAULT_TCP_LOGGING_PORT,
                 handler=LogRecordStreamHandler):
        socketserver.ThreadingTCPServer.__init__(self, (host, port), handler)
        self.abort = 0
        self.timeout = 1
        self.logname = None

    def serve_until_stopped(self):
        import select
        abort = 0
        while not abort:
            rd, wr, ex = select.select([self.socket.fileno()],
                                       [], [],
                                       self.timeout)
            if rd:
                self.handle_request()
            abort = self.abort

def main():
    logging.basicConfig(
        format='%(relativeCreated)5d %(name)-15s %(levelname)-8s %(message)s')
    tcpserver = LogRecordSocketReceiver()
    print('About to start TCP server...')
    tcpserver.serve_until_stopped()

if __name__ == '__main__':
    main()

```
실행은 다음과 같이 한다.
> python LogServer.py

그리고, 이것을 사용하려는 클라이언트(BDAE 의 Python Module 안에서)는 다음과 같이 사용한다.<br>
아래는 **sys.stdout,stderr** 등을 **Redirect** 하였기 때문에 **print(str(object))** 형태로 모두 출력할 수 <br>
있다는 점이다.
```
import pandas as pd
import numpy as np
import seaborn as sns
from StreamToLogger import StreamToLogger
import sys
import logging, logging.handlers

def describe(df):
    # 아래를 넣으면 원격 로그 서버에 들어간다.
    # 시작
    logger = logging.getLogger('TitanicDesc:describe')
    logger.setLevel(logging.DEBUG)

    socketHandler = logging.handlers.SocketHandler('localhost',
                    logging.handlers.DEFAULT_TCP_LOGGING_PORT)
    logger.addHandler(socketHandler)
    ##  이 부분은 print 를 위한 부분이다. Redirect
    sys.stdout = StreamToLogger(logger,logging.INFO)
    sys.stderr = StreamToLogger(logger,logging.ERROR)

    # 끝
    print('----- start -----')
    colums_ = df.columns.tolist()
    print(str(colums_))
    df.columns = list(map(str.lower,colums_))
    df_desc = df.describe()
    df_desc.reset_index(inplace=True)
    df_desc.columns = ['vars', 'passengerid', 'survived', 'pclass', 'age', 'sibsp', 'parch', 'fare']
    df_melt = pd.melt(df_desc, id_vars=['vars'])

    # 반드시 아래 두줄을 넣어야 한다.
    socketHandler.close()
    logger.removeHandler(socketHandler)

    return df_melt
```
