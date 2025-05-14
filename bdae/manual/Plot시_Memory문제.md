## Matplotlib 메모리 이슈

아래처럼 이미지를 1000 개 만들면 메모리 이슈가 발생한다.
```
import matplotlib.pyplot as plt
import numpy as np
import psutil

x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)

plt.close('all') # closes all the figure windows

for i in range(1000):
    if i % 100 == 0:
        print(str(i+1), 'turn with', str(psutil.virtual_memory())) # 메모리 사용량 기록
    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.savefig(str(i) + '.png') # figure 파일로 저장
```

아래 처럼 명시적으로 닫아 주면 된다.
```
import matplotlib.pyplot as plt
import numpy as np
import psutil

x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)

plt.close('all') # closes all the figure windows

for i in range(1000):
    if i % 100 == 0:
        print(str(i+1), 'turn with', str(psutil.virtual_memory())) # 메모리 사용량 기록
    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.savefig(str(i) + '.png') # figure 파일로 저장
    
    plt.cla()   # clear the current axes
    plt.clf()   # clear the current figure
    plt.close() # closes the current figure
```
