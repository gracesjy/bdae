## Explicit Logging

You may use flush() ...


```
   import logging

   logger = logging.getLogger()
   logger.setLevel(logging.INFO)
   formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(messages)s")
   file_handler = logging.FileHandler("/tmp/my.log")
   logger.addHandler(file_handler)
   
   for i in range(10):
	   logger.info("--------------------------aaa----------------------")
      
   file_handler.flush()

   # .....
   file_handler.close()
```
