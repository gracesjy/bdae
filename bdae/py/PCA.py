import pandas as pd 
import numpy as np 
from numpy import * 
import logging

def run_pca_2nd(df, ls1): 
    logging.basicConfig(filename="/tmp/pyarg.log", level=logging.DEBUG)
    logging.debug("type {} ".format(type(ls1)))
    logging.debug("data {} ".format(ls1))
    cols = list(df) 
    cols_output = cols[6:]; 
    numpy_matrix = df.values 
    refined_matrix = numpy_matrix[:,6:] 

    covMat = cov(refined_matrix.astype(float), rowvar=0) 
    eigVals,eigVects = linalg.eig(mat(covMat)) 
    retVals = eigVals.tolist() 
    data = {'PARAM' : cols_output, 'EIGVAL': retVals } 
    pdf = pd.DataFrame(data, columns=['PARAM','EIGVAL']) 
    logger = logging.getLogger()
    logger.handlers[0].flush()
    return (pdf) 
