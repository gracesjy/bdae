## Rcpp 를 R 에서 테스트 하려면

먼저 Rcpp 를 설치했다고 가정한다.<br>
1.  사용하려는 Rcpp 관련 소스를 Edit 한다.
  > 주의할 사항은  [[Rcpp::export]] 를 반드시 넣어야 한다.
  ```
   #include <Rcpp.h>
   using namespace Rcpp;

   // [[Rcpp::export]]
   NumericVector convolveCpp(NumericVector a, NumericVector b) {
     int na = a.size(), nb = b.size();
     int nab = na + nb - 1;
     NumericVector xab(nab);
     for (int i = 0; i < na; i++)
       for (int j = 0; j < nb; j++)
         xab[i + j] += a[i] * b[j];
     return xab;
  }
```

2.  R 을 실행 시킨 후 다음과 같이 한다.
  ```
  library(Rcpp)
  sourceCpp("convolveCpp.cpp")
  x = 1
  y = 2
  convolveCpp(x,y)
  ```
