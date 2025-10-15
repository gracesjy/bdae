## BDAE Python
### 개요
BDAE 는 Python 을 추천한다. 그 이유는 BDAE 는 C/C++ 기반으로 만들어졌고 예외처리를 할 때 R 보다는
Python 이 훨씬 더 효과적으로 TraceBack 이 잘 동작하기 때문이다.<br><br>
GPU 가 있다면 GPU 를 사용할 수 있고, 그것이 가능하다는 것을 Docker 나 독립적인 On-Premise 를 구축해서 테스트를 모두 했었다.  R 보다는 Python 이 GPU 친화적이다. <br><br>

### BDAE R 과 다른 점
BDAE R 과 Python 의 다른 점은 R 은 함수 이름 정도이지만, Python 은 모듈이름과 시작함수가 있어야 한다는 점이고 BDAE 테이블 함수가 ap 로 시작된다는 점이다.  나머지 개념은 동일하다. 이 모듈이름은 클래스가 아니다.<br>
