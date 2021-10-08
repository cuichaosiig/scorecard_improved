import pandas as pd
import numpy as np

def unique_counts(df,cols):
    '''
    # 显示各个列的唯一值个数：
    df: 需要进行处理的dataframe
    cols： 需要处理的列

    return:
    描述信息
    -------------------------------
    Author: 崔超
    '''

    uniqC = pd.DataFrame()
    uniqC = df.apply(lambda x: len(x.value_counts()) ,axis = 0)

    return uniqC

