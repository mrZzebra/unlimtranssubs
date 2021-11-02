import pandas as pd
import numpy as np
import source.support as spt
from sklearn.neighbors import KDTree
def matching (df_tgg, df_ctg,tip,starting_vintage = 24249):
    list_cg = []
    list_kg = []
    list_cl = []
    mnths =[]
    
    vints = df_tgg.MonthsSov_x.unique()
    vints = vints[vints >= starting_vintage]
    vints = list(vints)
    vints.sort()
    
    df_tgg_full = pd.DataFrame()
    df_ctg_full = pd.DataFrame()

    for vint in vints: 
        vint=int(vint)
        month = vint
        
        df = df_tgg[df_tgg['MonthsSov_x'] == vint]

        df_tgg_last2 = df[df.MonthsRD < month]
        df_tgg_last2 = df_tgg_last2[df_tgg_last2['MonthsRD'] >= month-2]
        df_ctg_last2 = df_ctg[df_ctg.MonthsRD < month]
        df_ctg_last2 = df_ctg_last2[df_ctg_last2['MonthsRD'] >= month-2]
        df_ctg_last2 = df_ctg_last2[(df_ctg_last2['MonthsSov_x'] > vint) | (df_ctg_last2['MonthsSov_x'] == 0)]

        df_tgg_last2 = df_tgg_last2.pivot_table(['kd_payment','SDO_sum','fee_amt'], ['client_tid'], 'MonthsRD').reset_index()
        df_ctg_last2 = df_ctg_last2.pivot_table(['kd_payment','SDO_sum','fee_amt'], ['client_tid'], 'MonthsRD').reset_index()

        df_tgg_mean10to5 = df[df.MonthsRD < month-5]
        df_tgg_mean10to5 = df_tgg_mean10to5[df_tgg_mean10to5['MonthsRD'] >= month-10]
        df_ctg_mean10to5 = df_ctg[df_ctg.MonthsRD < month - 5]
        df_ctg_mean10to5 = df_ctg_mean10to5[df_ctg_mean10to5['MonthsRD'] >= month-10]
        df_ctg_mean10to5 = df_ctg_mean10to5[(df_ctg_mean10to5['MonthsSov_x'] > vint)| (df_ctg_mean10to5['MonthsSov_x'] == 0)]

        if tip in [299, 749, 2499]:
            df_tgg_full_means = df_tgg_mean10to5.groupby(['client_tid']).agg({'kd_payment':'mean','fee_amt':'mean','SDO_sum':'mean'}).reset_index()
            df_ctg_full_means = df_ctg_mean10to5.groupby(['client_tid']).agg({'kd_payment':'mean','fee_amt':'mean','SDO_sum':'mean'}).reset_index()
        else:
            df_tgg_full_means = df_tgg_mean10to5.groupby(['client_tid']).agg({'kd_payment':'mean','SDO_sum':'mean'}).reset_index()
            df_ctg_full_means = df_ctg_mean10to5.groupby(['client_tid']).agg({'kd_payment':'mean','SDO_sum':'mean'}).reset_index()
            
            
        df_tgg_full_means = df_tgg_full_means.join(df_tgg_last2)
        df_ctg_full_means = df_ctg_full_means.join(df_ctg_last2)

        del df_tgg_full_means[('client_tid','')]
        del df_ctg_full_means[('client_tid','')]

        df_tgg_to_match = df_tgg_full_means.copy()
        df_ctg_to_match = df_ctg_full_means.copy()

        df_tgg_to_match = df_tgg_to_match.set_index('client_tid')
        df_ctg_to_match = df_ctg_to_match.set_index('client_tid')

        for col in df_tgg_to_match.columns:
            df_tgg_to_match[col] = df_tgg_to_match[col].fillna(0)
        for col in df_ctg_to_match.columns:
            df_ctg_to_match[col] = df_ctg_to_match[col].fillna(0)

        norm = pd.concat([df_tgg_to_match, df_ctg_to_match])

        mean = norm.mean(axis = 0)
        std = norm.std(axis = 0)

        df_tgg_to_match = (df_tgg_to_match - mean) / std
        df_tgg_to_match.fillna(0)

        df_ctg_to_match = (df_ctg_to_match - mean) / std
        df_ctg_to_match.fillna(0)

        tree = KDTree(df_ctg_to_match)
        mindist_jn, minid_jn = tree.query(df_tgg_to_match,)
        np.minid_jn = minid_jn
        int_minid_jn = list(map(int, minid_jn))

        df_new_ctg_1 = pd.DataFrame()
        df_new_ctg_1['client_tid'] = df_ctg_to_match.loc[df_ctg_to_match.index[int_minid_jn]].reset_index().client_tid
        df_new_ctg_1['mindist'] = mindist_jn
        df_new_ctg_1 = df_new_ctg_1.merge(df_ctg, how = 'left', on = ['client_tid'])

        df_tgg_to_matchl_1 = list(df_tgg_to_match.index)
        df_tgg_1 = df_tgg[(df_tgg['client_tid'].isin(df_tgg_to_matchl_1)) & (df_tgg['MonthsSov_x'].isna() == False)]

        df_corr = pd.DataFrame()
        df_corr['df_ctg'] = df_ctg_to_match.loc[df_ctg_to_match.index[int_minid_jn]].reset_index().client_tid
        df_corr['df_tgg'] = df_tgg_to_matchl_1

        exec("n_clients_{} = len(df_tgg_1.client_tid.value_counts())".format(vint))

        df_new_ctg_1_means = df_new_ctg_1.groupby('MonthsRD').mean().reset_index()
        df_tgg_1_means = df_tgg_1.groupby('MonthsRD').mean().reset_index()
        
        exec("df_ctg_{} = df_new_ctg_1_means".format(vint))
        exec("df_tgg_{} = df_tgg_1_means".format(vint))

        mnths.append(vint)

        exec("df_tgg_{} = spt.months_to_date(df_tgg_{},'MonthsRD')".format(vint,vint))
        exec("df_ctg_{}['MonthsRD'] = df_ctg_{}['MonthsRD'].astype(int)".format(vint,vint))
        exec("df_ctg_{} = spt.months_to_date(df_ctg_{},'MonthsRD')".format(vint,vint))

        exec("list_kg.append(df_ctg_{})".format(vint))
        exec("list_cg.append(df_tgg_{})".format(vint))
        list_cl.append(len(df_tgg_1.client_tid.value_counts()))
        

        df['treatment'] = vint 
        df['t'] = df['MonthsRD'] - vint 
        df_tgg_full = pd.concat([df_tgg_full,df])
        
        df_new_ctg_1['treatment'] = vint 
        df_new_ctg_1['t'] = df_new_ctg_1['MonthsRD'] - vint 
        df_ctg_full = pd.concat([df_ctg_full,df_new_ctg_1])
        
    return(df_tgg_full,df_ctg_full,list_cg,list_kg,list_cl,mnths)