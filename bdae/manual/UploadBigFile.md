### Big File Upload

```
   28  git lfs install
   29  ls -rtl
   30  git lfs track "*.001"
   31  git add .gitattributes
   32  git add *.001
   33  git commit -m "big file"
   34  git push
   35  git push --set-upstream origin master
   36  git lfs install
   37  git lfs track "*.002"
   38  git add *.002
   39  git commit -m "big file2"
   40  git push --set-upstream origin master
   41  dir
   42  git lfs install
   43  git lfs track "redis_prep.zip"
   44  git add redis_prep.zip
   45  git commit -m "python packages"
   46  git push --set-upstream origin master
   47  git lfs install
   48  git lfs track "redis-server.tar"
   49  git add redis-server.tar
   50  git commit -m "real big file"
   51  git push --set-upstream origin master

```

https://github.com/gracesjy/handsonml2/tree/master
