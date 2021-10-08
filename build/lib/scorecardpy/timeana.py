import datetime
import pandas as pd
import numpy as np


def time_shift(df,col,analist = ['year','month','dayofweek']):
    '''
    # 对时间进行处理 
    df: 需要进行处理的dataframe
    col： 需要处理的列
    analist: 需要提取的时间要素
        默认:
        year,month,dayofweek

    return:
    增加了时间序列的函数
    除去dayofweek之外，增加了从1970-01-01到时间的天数
    -------------------------------
    Author: 崔超
    '''

    df[f'{col}'] = pd.to_datetime(df[col])
    for ana in analist:
        df[f'{col}_{ana}'] = eval(f'df[col].dt.{ana}')
    base_time = datetime.datetime.strptime('1970-01-01', '%Y-%m-%d')
    df[f'{col}_strfsd'] = df[col].apply(lambda x: x-base_time).dt.days
    #df.drop(col, axis = 1, inplace = True)

    return df
