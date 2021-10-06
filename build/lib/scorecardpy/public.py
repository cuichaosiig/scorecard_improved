import pandas as pd
import numpy as np
from .woebin import woebin

bfunclist = {
        'abs':'''lambda y: f"lambda x: x['{y}'].apply(np.abs)"''',
        'babs':
        '''lambda y: f"lambda x: x['{y}'].apply(lambda z:1 if z>0 else -1 if z<0 else 0)"''',
        'zeroornot':
        '''lambda y: f"lambda x: x['{y}'].apply(lambda z:1 if z!=0 else 0)"''',
        }

iv_threshold=0.1

def transfer_apply(df,validfunc):

    '''
    df : 进行转化的dataframe
    validfunc: list of 见 transfer_2d
        [有效的转化参数名称，[其他,lambda 函数 string 字符串],iv]

    return:
    转化后的df

    -------------------------------
    Author: 崔超
    '''
    for i in validfunc:
        if isinstance(i,list) and isinstance(i[1],list):
            df [i[0]] = eval(i[1][1])(df)

    return df

def get_validtrans(df,yname,funclist,pardict,lambda_list):
    '''
    #进行有效指标函数的筛选
    df: 函数生成的dataframe
    yname: label列名称
    funclist: 函数名称->函数定义的lambda函数（dict）
    pardict: 参数字典
    lambda_list: lambda函数列表

    return:
    lambda_list

    -------------------------------
    Author: 崔超
    '''
    # Get dataframe
    gen_df = pd.DataFrame({'y':df[yname]})
    for i in sorted(funclist.keys()):
        gen_df[i] = eval(funclist[i])(df)
        # 为了节省资源负担，当列数量>50时则进行一次检查
        if len(gen_df.columns)>200 or i == sorted(funclist.keys())[-1] : 
            # Do IV Ana:
            bins = woebin(gen_df,y='y')

            # Filter the valid one
            best_trans = [ 
                [key,[pardict,funclist[key]],bins[key].total_iv.values[0]] 
                for key in bins.keys()
                ]
            # 剔除有效指标IV 过低或者不需要进行转换的指标
            valid_trans = [i for i in best_trans if (i[2]>iv_threshold)  ] 
            lambda_list += valid_trans
            print(f'{len(valid_trans)} added, now {len(lambda_list)}')
            # Reset
            gen_df = pd.DataFrame({'y':df[yname]})
    return lambda_list

def transferfunclist(funclist,pardict,lambda_list):
    '''
    #将lambda函数字段转化为标准输出
    funclist: 函数名称->函数定义的lambda函数（dict）
    pardict: 参数字典
    lambda_list: lambda函数列表

    return:
    lambda_list

    -------------------------------
    Author: 崔超
    '''

    lambda_list.extend([ 
                [key,[pardict,funclist[key]],1] 
                for key in funclist
                ])
    return lambda_list
