import pandas as pd
import numpy as np
from .public import *

def discrete_encode(df,col,method='index',lambda_list = []):
    '''
    # 对离散值（字符串等）进行编码：
    df: 需要进行处理的dataframe
    col： 需要处理的列
    method: 进行处理的方法:
        当前支持的方法:
        index: 按照0-n的方式进行编码，按照数量从多到少进行编码
    lambda_list: 初始化的lambda函数列表,
        [有效的转化参数名称，[其他,lambda 函数 string 字符串],iv]

    return:
    函数集合
    [有效的转化参数名称，[其他,lambda 函数 string 字符串],iv]
    -------------------------------
    Author: 崔超
    '''

    funclist = {}
    parlist = {}
    if type(col) is list:
        cols = col
    else:
        cols = [cols]

    if method == 'index':
        for col in cols:
            distinct_values = df[col].value_counts().index
            map_dict = dict(zip(distinct_values,range(len(distinct_values))))
            
            funclist[f'{col}_mapped'] = f'lambda df,pardict: df["{col}"].map(pardict["mapdict"])'
            parlist[f'{col}_mapped'] = dict() 
            parlist[f'{col}_mapped']['pars'] = {'mapdict':map_dict}
            parlist[f'{col}_mapped']['usepar'] = True
    
    lambda_list = transferfunclist(funclist,parlist,lambda_list,multiple=1)

    return lambda_list
