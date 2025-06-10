### R Coding Style for BDAE

이 형태의 것을 추천한다. 그 이유는 다양한 함수들을 만들고 즉시 호출하면서 <br>
마치 개발할 때와 동일한 형태를 유지할 수 있기 때문이다. <br><br>

단, data, args 를 변수명으로 사용하지 말자. 이 두개는 BDAE 가 사용한다.
```
library(logr)

log_open("/tmp/rlog.log")
log_print('------ start -------')
log_print(str(data))
log_print(str(args))

# your own function
my <- function() {
   a <- 99.99  
   return (a)
}

aa = c('aaaaaaaaaa','ccccccc')

# call your function
k <- my()
bb = c(k, 22.12)

df <- data.frame(A=aa,B=bb,stringsAsFactors=FALSE)
kkk <- 939.999
df

```
