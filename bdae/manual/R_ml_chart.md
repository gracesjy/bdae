### R Chart 

R Code saved as R_ml_chart
```
# set SCRIPT_TYPE -> NEW_TYPE

library(kohonen)
library(jpeg)
library(logr)
library(htmltools)
library(RCurl)
log_open("/tmp/rlog.log")

train  <- sample(1:150, 100) ;
train_set  <-  list(x = as.matrix(iris[train,-5]), Species = as.factor(iris[train,5])) 
test_Set <- list(x = as.matrix(iris[-train,-5]), Species = as.factor(iris[-train,5])) 
gr <- somgrid(xdim = 3, ydim = 5, topo = "hexagonal") #grid 갯수 및 모양 설정
ss <- supersom(train_set, gr, rlen = 200, alpha = c(0.05, 0.01)) #som 학습하기

my<-function(img_file) {
   log_print('in my() function ..')
   log_print(paste('file_name : ', img_file))
   log_print(paste('file_size : ', file.info(img_file)[1, "size"]))
	zz <- file(img_file, "rb")
	jpg1_lraw.lst <- vector("list", 1)
	jpg1_lraw.lst[[1L]] <- readBin(zz, "raw", file.info(img_file)[1, "size"])
	close(zz)

	df <- data.frame(name=img_file,stringsAsFactors=FALSE)
	df$blob <- jpg1_lraw.lst
   
   unlink(img_file)
	return (df)
}

name <- c("/tmp/kohonen01.jpg","/tmp/kohonen02.jpg","/tmp/kohonen03.jpg","/tmp/kohonen04.jpg", "/tmp/kohonen05.jpg")

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
jpeg(name[5])
plot(ss, type="codes", shape = "straight")
dev.off()

df = my(name[1])
for (i in 2:length(name)) {
   df_tmp = my(name[i])
   log_print(name[i])
   df = rbind(df, df_tmp)
}

df
```

SQL
```
SELECT * 
   FROM 
   table(asEval( 
   NULL, 
   'SELECT CAST(''AA'' AS VARCHAR2(100)) name,
           TO_BLOB(NULL) img
    FROM dual', 
   'R_ml_chart'))
```
