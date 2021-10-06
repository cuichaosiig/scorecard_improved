import datetime
import pandas as pd
import numpy as np


def time_shift(df,col):
    '''
    # 对时间进行处理 
    df: 需要进行处理的dataframe
    col： 需要处理的列

    return:
    增加了时间序列的函数
    年份
    月份
    从1970-01-01到时间的天数
    -------------------------------
    Author: 崔超
    '''

    df[f'{col}'] = pd.to_datetime(df[col])
    df[f'{col}_y'] = df[col].dt.year
    df[f'{col}_m'] = df[col].dt.month
    base_time = datetime.datetime.strptime('1970-01-01', '%Y-%m-%d')
    df[col] = df[col].apply(lambda x: x-base_time).dt.days
    #df.drop(col, axis = 1, inplace = True)

    return df
