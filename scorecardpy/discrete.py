import pandas as pd
import numpy as np
from .public import *

def discrete_encode(df,col,method='index',lambda_list = []):
    '''
    # 对离散值（字符串等）进行编码：
    df: 需要进行处理的dataframe
    col： 需要处理的列,list or str
    method: 进行处理的方法:
        当前支持的方法:
        index: 按照0-n的方式进行编码，按照数量从多到少进行编码
        sort: 按照0-n的方式进行编码，按照字符串排序指定 
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

    for col in cols:
        distinct_values = df[col].value_counts().index
        distinct_values_count = df[col].value_counts().values
        map_dict = {}
        if method == 'index':
            map_dict = dict(zip(distinct_values,distinct_values_count))
        if method == 'sort':
            map_dict = dict(zip(sorted(distinct_values),range(len(distinct_values))))

        if len(map_dict) < 2:
            raise Exception('Size of the mapDict is 0 or 1')
            
        funclist[f'{col}_mapped'] = f'lambda df,pardict: df["{col}"].map(pardict["mapdict"])'
        parlist[f'{col}_mapped'] = dict() 
        parlist[f'{col}_mapped']['pars'] = {'mapdict':map_dict}
        parlist[f'{col}_mapped']['usepar'] = True

    
    lambda_list = transferfunclist(funclist,parlist,lambda_list,multiple=1)

    return lambda_list

def discrete_encode_c(df,col_d,col_c,method='mean',lambda_list = []):
    '''
    # 对离散值(数值型或者字符串型)进行编码，与连续值进行联合编码：
    df: 需要进行处理的dataframe
    col_d: 需要处理的离散值列,list or str
    col_c: 需要处理的连续值列,list or str
    method: 进行处理的方法:
        当前支持的方法,标准的agg需求函数
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
    for i in col_d:
        dgroup = df.groupby(i)
        for j in col_c:
            map_dict = dgroup[j].agg(method).to_dict()
            key = i
            if type(i) is list:
                key = '-'.join(i)
            funclist[f'{key}_{j}_{method}'] = f'lambda df,pardict: df["{key}"].map(pardict["mapdict"])'
            parlist[f'{key}_{j}_{method}'] = dict() 
            parlist[f'{key}_{j}_{method}']['pars'] = {'mapdict':map_dict}
            parlist[f'{key}_{j}_{method}']['usepar'] = True

    lambda_list = transferfunclist(funclist,parlist,lambda_list,multiple=1)

    return lambda_list


