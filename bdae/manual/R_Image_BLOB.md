### R 차트 이미지 관련
plotly 말고, 이미지 포맷에 대한 것은 바이너리(BLOB) 이 가장 작은 사이즈이다.<br>
고전적인 것이니 참고 하면 좋겠다.<br>
<br>

아래는 R 에서 제공하는 보통 참조하는 라이브러리이다.
```
library(kohonen)
library(jpeg)
library(logr)
library(htmltools)
library(RCurl)
```
먼저 이미지는 Machine Learning 예를 참조 했으니 다음을 추가한다.
```
train  <- sample(1:150, 100) 
train_set  <-  list(x = as.matrix(iris[train,-5]), Species = as.factor(iris[train,5])) 
test_Set <- list(x = as.matrix(iris[-train,-5]), Species = as.factor(iris[-train,5])) 
gr <- somgrid(xdim = 3, ydim = 5, topo = "hexagonal") #grid 갯수 및 모양 설정
ss <- supersom(train_set, gr, rlen = 200, alpha = c(0.05, 0.01)) #som 학습하기
```
위의 ss 로 이미지 파일을 생성하려면 다음과 같이 하면 된다. <br>
고전적인 ggplot 이나 plot 은 다음과 같이 파일로 일단 만들고, data.frame 화 한 후 unlink 로 삭제제.<br>
```
name <- c("/tmp/kohonen01.jpg","/tmp/kohonen02.jpg","/tmp/kohonen03.jpg","/tmp/kohonen04.jpg")

jpeg(name[1])
plot(ss,type="changes")
dev.off()
jpeg(name[2])
plot(ss, type="count", main="Node Counts")
dev.off()
jpeg(name[3])
plot(ss, type="dist.neighbours", main = "SOM neighbour distances", shape = "straight")
dev.off()
jpeg(name[4])
plot(ss, type="dist.neighbours", palette.name=grey.colors, shape = "straight")
dev.off()
```

이것을 data.frame 으로 만드는 함수는 다음 처럼 하면 된다.
```
my<-function(img_file) {
	zz <- file(img_file, "rb")
	jpg1_lraw.lst <- vector("list", 1)
	jpg1_lraw.lst[[1L]] <- readBin(zz, "raw", file.info(img_file)[1, "size"])
	close(zz)

	df <- data.frame(name=img_file,stringsAsFactors=FALSE)
	df$blob <- jpg1_lraw.lst
	# 파일 삭제   
	unlink(img_file)
	return (df)
}
```
앞의 모든 이미지를 묶는 것은 다음과 같이 해 보았다.
```
df = my(name[1])
for (i in 2:length(name)) {
   df_tmp = my(name[i])
   df = rbind(df, df_tmp)
}
```


