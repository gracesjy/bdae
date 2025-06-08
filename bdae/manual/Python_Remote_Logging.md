## <p>$\bf{\large{\color{#6580DD}BDAE 원격 로그 남기기}}$</p>

먼저 본 manual 의 로그서버를 띄운다. LogServer.md 를 복사해서 ..<br>
그리고 BDAE 에 등록되는 Python Module 의 맨 앞과 뒤에 다음을 넣는다.<br>

```
import pandas as pd
import numpy as np
import seaborn as sns

## 아래 3개의 import 가 로깅을 위한 것이다.
from StreamToLogger import StreamToLogger
import sys
import logging, logging.handlers
## 

## 등록되는 함수
def describe(df):
    # 아래를 넣는다.
    logger = logging.getLogger('TitanicDesc:describe')
    logger.setLevel(logging.DEBUG)
    socketHandler = logging.handlers.SocketHandler('localhost',
                    logging.handlers.DEFAULT_TCP_LOGGING_PORT)
    logger.addHandler(socketHandler)
    
    sys.stdout = StreamToLogger(logger,logging.INFO)
    sys.stderr = StreamToLogger(logger,logging.ERROR)
    
    print('----- start -----')

    # .... 알고리즘 부분 이다.
    # print(str(Object)) 를 사용하면 편리하다.

    print('----- end -----')

    # 아래 2줄이 빠지면 중복해서 기록되니 반드시 해라.
    socketHandler.close()
    logger.removeHandler(socketHandler)
    
    return df_melt
```
