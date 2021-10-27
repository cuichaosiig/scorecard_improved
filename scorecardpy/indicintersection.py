
import pandas as pd
import numpy as np
from .woebin import woebin
from .public import get_validtrans
from .public import bfunclist

def admd(df,topcols,yname,lambda_list=[],topcols2=[]):
    '''
    # 批量进行指标的加减乘除
    df: 进行转化的dataframe 
    topcols: 需要进行交叉的指标集合
    topcols2: 需要进行交叉的指标集合,如果不输入则topcols自己搞
    yname: label 列
    lambda_list: 转换函数列

    note:
    新增指标做了woe的过滤(>0.02)，通过woebin进行处理

    return:
    函数集合
    [有效的转化参数名称，[角度,lambda 函数 string 字符串],iv]
    -------------------------------
    Author: 崔超
    '''
    if len(topcols2)==0:
        topcols2 = topcols
    # Get the function list
    funclist = {}
    for i in topcols:
        for j in topcols2:
            if '({i})+({j})' not in funclist.keys() and '({j})+({i})' not in funclist.keys() and i!=j: 
                funclist[f'({i})+({j})'] = f"lambda df: df['{i}']+df['{j}']"
                funclist[f'({i})-({j})'] = f"lambda df: df['{i}']-df['{j}']"
                funclist[f'({i})*({j})'] = f"lambda df: df['{i}']*df['{j}']"
    
    for i in topcols:
        for j in topcols2:
            if i!=j:
                funclist[f'({i})/({j})'] = f"lambda df: df['{i}']/(df['{j}']+0.00001)"
    lambda_list = get_validtrans(df,yname,funclist,{'admd':-1},lambda_list)

    return lambda_list

#def indicpos_add(df,topcols,yname,lambda_list=[],topcols2=[]):
#    '''
#    # 批量进行指标的交、并运算
#    df: 进行转化的dataframe 
#    topcols: 需要进行交叉的指标集合
#    topcols2: 需要进行交叉的指标集合,如果不输入则topcols自己搞
#    yname: label 列
#    lambda_list: 转换函数列
#
#    note:
#    新增指标做了woe的过滤(>0.02)，通过woebin进行处理
#
#    return:
#    函数集合
#    [有效的转化参数名称，[角度,lambda 函数 string 字符串],iv]
#    -------------------------------
#    Author: 崔超
#    '''
#    #生成topcols字典
#    funclist = {'zeroornot_'+i:eval(bfunclist['zeroornot'])(i) for i in topcols}
#    lambda_list.extend(funclist)
#    # 生成funclist2字典 
#    funclist2 = {}
#    if topcols2 != []:
#        funclist2 = {'zeroornot_'+i:eval(bfunclist['zeroornot'])(i) for i in topcols2}
#        lambda_list.extend(funclist2)
#    else:
#        funclist2 = funclist
#    # 生成df
#    gen_df = pd.DataFrame({'y':df[yname]})
#    for i in funclist:
#        gen_df[i] = eval(funclist[i])(df) 
#
#    if topcols2 != []:
#        for i in funclist2:
#            if i not in gen_df.columns:
#                gen_df[i] = eval(funclist2[i])(df) 
#    # 生成交叉指标
#    funclist_2d = {}
#    for i in funclist.keys():
#        for j in funclist2.keys():
#            funclist_2d[f'{i}.add{j}'] = f"lambda df: df['{i}']+df['{j}']"
#
#    print(gen_df)
#    lambda_list = get_validtrans(gen_df,'y',funclist_2d,{'indicpos_add':-1},lambda_list)
#
#    return lambda_list
