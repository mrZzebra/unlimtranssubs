import pandas as pd
import numpy as np 

def count_months(column):
    column = column.str.replace('?','00.00.0000')
    df_tmp = column.str.split('.', expand = True)
    df_tmp[1] = df_tmp[1].fillna('0')
    df_tmp[2] = df_tmp[2].fillna('0')
    df_tmp[1] = df_tmp[1].astype(int)
    df_tmp[2] = df_tmp[2].astype(int)
    new_col = df_tmp[2] * 12 + df_tmp[1] 
    return(new_col)

def months_to_date(df,months_col):
    df['01'] = '01'
    df['glue'] = '-'
    df['mth'] = df[months_col] % 12
    df['yr'] = df[months_col] // 12
    df['yr'] = df['yr'].mask(df['mth'] == 0,df['yr']-1)
    df['mth'] = df['mth'].mask(df['mth'] == 0,12)
    df['date'] = df['01'] + df['glue'] + df['mth'].astype(str) + df['glue'] + df['yr'].astype(str)
    df['date'] = pd.to_datetime(df['date'], dayfirst=True)
    return(df.set_index('date'))

def mask_0(dfcolumn):
    dfcolumn = dfcolumn.mask(dfcolumn < 0,0)
    return(dfcolumn)

def red_line_date(month_num):
    m = month_num % 12
    y = month_num // 12
    if m == 0:
        y = y - 1
        m = 12
    str_date = '01-' + str(m) + '-' + str(y)
    return(str_date)

def spread_comission(df_subs_half):
    df_subs_half = df_subs_half.sort_values(by = ['client_tid','MonthsRD']).reset_index()
    df_subs_half['sum_monthly'] = 0
    
    sum_list = ['199','299','499','749','1599','2499','99.67','199.33','249.67','499.33','1666','833']

    for s in sum_list:
        df_subs_half[s] = df_subs_half['summa_pokupki'][df_subs_half['summa_pokupki'] == float(s)]

    df_subs_half['99'] = df_subs_half['summa_pokupki'][df_subs_half['summa_pokupki'].isin([99,198,297,396])]

    df_subs_half[sum_list] = df_subs_half[sum_list].fillna(0)
    
    a_1599 = (df_subs_half['1599'] + df_subs_half['1599'].shift(1) + df_subs_half['1599'].shift(2) + df_subs_half['1599'].shift(3)+df_subs_half['1599'].shift(4)+df_subs_half['1599'].shift(5)
    + df_subs_half['1599'].shift(6) + df_subs_half['1599'].shift(7) + df_subs_half['1599'].shift(8)
    + df_subs_half['1599'].shift(9) + df_subs_half['1599'].shift(10) + df_subs_half['1599'].shift(11))
    a_2499 = (df_subs_half['2499'] + df_subs_half['2499'].shift(1) + df_subs_half['2499'].shift(2) + df_subs_half['2499'].shift(3)+df_subs_half['2499'].shift(4)+df_subs_half['2499'].shift(5)
    + df_subs_half['2499'].shift(6) + df_subs_half['2499'].shift(7) + df_subs_half['2499'].shift(8)
    + df_subs_half['2499'].shift(9) + df_subs_half['2499'].shift(10) + df_subs_half['2499'].shift(11))
    a_499 = df_subs_half['499'] + df_subs_half['499'].shift(1) + df_subs_half['499'].shift(2)
    a_749 = df_subs_half['749'] + df_subs_half['749'].shift(1) + df_subs_half['749'].shift(2)
    
    df_subs_half['1599'] = np.where((a_1599==1599) & (df_subs_half['MonthsSov_x'] <= df_subs_half['MonthsRD']),
                                      133.25,df_subs_half['1599'])
    df_subs_half['2499'] = np.where((a_2499==2499) & (df_subs_half['MonthsSov_x'] <= df_subs_half['MonthsRD']),
                                          208.25,df_subs_half['2499'])
    df_subs_half['499'] = np.where((a_499==499) & (df_subs_half['MonthsSov_x'] <= df_subs_half['MonthsRD']),
                                          166.33,df_subs_half['499'])
    df_subs_half['749'] = np.where((a_749==749) & (df_subs_half['MonthsSov_x'] <= df_subs_half['MonthsRD']),
                                      249.67,df_subs_half['749'])
    
    df_subs_half['sum_monthly']  = (df_subs_half['199'] + df_subs_half['299'] + df_subs_half['499']
    + df_subs_half['749'] + df_subs_half['1599'] + df_subs_half['2499'] + df_subs_half['99'])
    
    return(df_subs_half)