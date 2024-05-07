import pandas as pd
import numpy as np

def returnNAN():
    df = pd.DataFrame([['motor type',1, np.inf],
                      [np.nan, 2, 3.2],
                      ['RF', np.nan, 4.5]],
                      columns = list('abc'))
    return df
