## R 기초
https://github.com/PacktPublishing/Machine-Learning-with-R-Fourth-Edition

data.frame 변환 예제들을 최대한 수렴하기 위해서 적는다.
```
# create sample data frame
set.seed(1234)

df <- data.frame(
  col1 = rnorm(5, mean = 5),
  col2 = rnorm(5, mean = 10)
)

# view data
head(df)
```
위의 summary 는 ?
```
> summary(df)
      col1            col2       
 Min.   :2.654   Min.   : 9.110  
 1st Qu.:3.793   1st Qu.: 9.425  
 Median :5.277   Median : 9.436  
 Mean   :4.648   Mean   : 9.586  
 3rd Qu.:5.429   3rd Qu.: 9.453  
 Max.   :6.084   Max.   :10.506  
> 
```

이것을 다음으로 정리하면 ?
```
new_df <- data.frame(do.call(cbind, lapply(df, summary)))

            col1      col2
Min.    2.654302  9.109962
1st Qu. 3.792934  9.425260
Median  5.277429  9.435548
Mean    4.647646  9.586039
3rd Qu. 5.429125  9.453368
Max.    6.084441 10.506056

# data type
class(new_df)
[1] "data.frame"
```

이것을 melt 하면 BDAE 로 줄 수 있다.
```
> new_df_df <- cbind(vars_name=rownames(new_df), new_df)
> new_df_df
        vars_name     col1      col2
Min.         Min. 2.654302  9.109962
1st Qu.   1st Qu. 3.792934  9.425260
Median     Median 5.277429  9.435548
Mean         Mean 4.647646  9.586039
3rd Qu.   3rd Qu. 5.429125  9.453368
Max.         Max. 6.084441 10.506056

> library(reshape)
> df_unpivot = melt(new_df_df,id=c('vars_name'))
> df_unpivot
   vars_name variable     value
1       Min.     col1  2.654302
2    1st Qu.     col1  3.792934
3     Median     col1  5.277429
4       Mean     col1  4.647646
5    3rd Qu.     col1  5.429125
6       Max.     col1  6.084441
7       Min.     col2  9.109962
8    1st Qu.     col2  9.425260
9     Median     col2  9.435548
10      Mean     col2  9.586039
11   3rd Qu.     col2  9.453368
12      Max.     col2 10.506056

```
어떤 model 을 data.frame 으로 하려면 ? <br>
예를 들면 아래와 같은 것.
```
house_lm <- lm(AdjSalePrice ~ SqFtTotLiving + SqFtLot + Bathrooms +
                 Bedrooms + BldgGrade,
               data=house, na.action=na.omit)
```
이 house_lm 을 data.frame 으로 만들어 보자. <br>
http://varianceexplained.org/r/broom-intro/
```
> library(broom)
> df_house_lm <- tidy(house_lm)
> df_house_lm
# A tibble: 6 × 5
  term              estimate  std.error statistic   p.value
  <chr>                <dbl>      <dbl>     <dbl>     <dbl>
1 (Intercept)   -521925.     15651.       -33.3   4.23e-238
2 SqFtTotLiving     229.         3.90      58.7   0        
3 SqFtLot            -0.0605     0.0612    -0.989 3.23e-  1
4 Bathrooms      -19438.      3625.        -5.36  8.32e-  8
5 Bedrooms       -47781.      2489.       -19.2   1.86e- 81
6 BldgGrade      106117.      2396.        44.3   0        

```

### list
```
> names(l1)
> for (p in l1) {
  print(p)
}
> for (i in 1:length(l1)) {
  print(as.data.frame(l1[[i]]))
  print(l1[[i]])
}

```
