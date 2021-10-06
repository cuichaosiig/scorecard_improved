import pandas as pd
import numpy as np
from .public import bfunclist 
from .public import (get_validtrans,transferfunclist)

def mathtrans(df,topcols,yname,method,lambda_list=[],dovalid=1): 
    '''
    #批量进行指标数学转换
    df: 进行转化的dataframe 
    topcols: 需要进行数学转换的指标集合
    yname: label 列
    lambda_list: 转换函数列
    method: 转换方法 'name|name'
        当前支持的函数见:
        sc.public.bfunclist
    dovalid: 是否通过IV分析进行关键指标过滤
        在数据比较稀疏的情况下，iv过滤会筛除该类数据
        在某些情况下，两个数据进行admd可能会生成新的指标，调用该方法后再调用admd，可能会有新的发现

    return:
    函数集合
    [有效的转化参数名称，[角度,lambda 函数 string 字符串],iv]
    -------------------------------
    Author: 崔超
    '''
    funclist = {i+'_'+j:eval(bfunclist[i])(j) \
            for i in method.split('|') \
                    for j in topcols \
                    if i in bfunclist.keys()}
    if dovalid==1:
        lambda_list = get_validtrans(df,yname,funclist,{'mathtrans':-1},lambda_list)
    else:
        lambda_list = transferfunclist(funclist,pardict,lambda_list)
        
    # Get the function list
    return lambda_list
