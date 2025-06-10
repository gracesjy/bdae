### R Image File to Base64

R code
```
function(){
  #comment
  png(tf1 <- tempfile(fileext = ".png"))
  res <- 1:10
  plot( 1:100, rnorm(100), pch = 21,bg = "red", cex = 2 )
  dev.off()
  library(RCurl)
  txt <- base64Encode(readBin(tf1, "raw", file.info(tf1)[1, "size"]), "txt")
  unlink(tf1)
  all <- paste("<div><img src='data:image/png;base64, ", txt, "' /></div>")
  xx <- c(all);
  name <- tf1
  mm <- data.frame(name, xx, stringsAsFactors=FALSE)
  mm
}
```

SQL
```
SELECT * 
   FROM 
   table(asEval( 
   NULL, 
   'SELECT CAST(''AA'' AS VARCHAR2(40)) name,
           TO_CLOB(NULL) img 
    FROM dual', 
   'R_base64'))
```
