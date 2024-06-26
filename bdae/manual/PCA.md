## PCA - Machine Learning in Action book

```
from numpy import *
import numpy as np
import pandas as pd

def pca(dataMat, topNfeat=9999999):
    meanVals = dataMat.mean(0)
    meanRemoved = dataMat - meanVals #remove mean
    covMat = cov(meanRemoved, rowvar=0)
    eigVals,eigVects = linalg.eig(mat(covMat))
    eigValInd = argsort(eigVals)            #sort, sort goes smallest to largest
    eigValInd = eigValInd[:-(topNfeat+1):-1]  #cut off unwanted dimensions
    redEigVects = eigVects[:,eigValInd]       #reorganize eig vects largest to smallest
    lowDDataMat = meanRemoved * redEigVects#transform data into new dimensions    
    reconMat = (lowDDataMat * redEigVects.T) + meanVals
    return lowDDataMat, reconMat

def detect(df):
    new_df = df.pivot(index='SEQUENCE', columns='VARIABLE', values='VALUE')
    dataMat = np.matrix(new_df.to_numpy())
    meanVals = mean(dataMat, 0)
    meanRemoved = dataMat - meanVals
    covMat = cov(meanRemoved, rowvar=0)
    eigVals, eigVects = linalg.eig(mat(covMat))

    xx = eigVals.sum()
    zz = eigVals.tolist()

    per = []
    for x in range(len(zz)):
        per.append(zz[x]/xx * 100)

    dictData = {'Param Name': new_df.columns.tolist(), 'Value(%)': per}
    pdf = pd.DataFrame(dictData)
    return pdf

```

SQL
```
SELECT * 
      FROM table(apTableEval(
         	cursor(SELECT * FROM PCA_TEST ORDER BY VARIABLE, SEQUENCE),
         	NULL,
            'SELECT CAST(''A'' AS VARCHAR2(40)) PARAMETER, 1.0 VALUE FROM DUAL',
           'PCASemi:detect'))
```
