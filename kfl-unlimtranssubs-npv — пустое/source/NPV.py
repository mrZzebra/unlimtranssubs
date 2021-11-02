def NPV_tail(df_NPV):
    operational_costs = 0
    income_tax_rate = 0.2
    discount_rate = 0.13
    
    df_NPV['income_tax'] = -df_NPV['income_before_tax'] * income_tax_rate
    df_NPV['cash_flow'] = df_NPV['income_before_tax'] + df_NPV['income_tax']

    df_NPV['discount_cash_flow'] = df_NPV['cash_flow'] / ((1 + ((1 + discount_rate) ** (1 / 12) - 1)) ** (df_NPV.index - 0.5))
    df_NPV['discount_cash_flow'].loc[0] = df_NPV['cash_flow'].loc[0]
    
    return(df_NPV['discount_cash_flow'].loc[range(0,df_NPV.index[-1] + 1)].sum(),df_NPV)
    
def NPV_299(df_tgg_full, df_ctg_full,periods,df_NPV_XX):
    df_tgg_NPV = df_tgg_full.groupby(['t']).mean().reset_index()
    df_ctg_NPV = df_ctg_full.groupby(['t']).mean().reset_index()
    df_NPV = df_tgg_NPV[['t','summa_pokupki','kd_payment','fee_amt']].merge(df_ctg_NPV[['t','summa_pokupki','kd_payment','fee_amt']], how='left', on='t')
    df_NPV = df_NPV.set_index('t')
    
    df_NPV = df_NPV.reindex(df_NPV.index.union(range(df_NPV.index[-1],0 + periods)))
    df_NPV['life_month'] = range(0,len(df_NPV))
    df_NPV['summa_pokupki_delta'] = df_NPV['summa_pokupki_x'] - df_NPV['summa_pokupki_y']
    df_NPV['summa_pokupki_delta'] = df_NPV['summa_pokupki_delta'].fillna(df_NPV['summa_pokupki_delta'].loc[range(4,7)].mean())

    df_NPV['kd_payment_corr'] = df_NPV['kd_payment_x'].loc[range(-3,0)].mean() - df_NPV['kd_payment_y'].loc[range(-3,0)].mean()
    df_NPV['kd_payment_delta'] = df_NPV['kd_payment_x'] - df_NPV['kd_payment_y'] - df_NPV['kd_payment_corr']
    df_NPV.loc[0,'kd_payment_delta'] = 0
    df_NPV['kd_payment_delta'] = df_NPV['kd_payment_delta'].fillna(df_NPV['kd_payment_delta'].loc[range(4,7)].mean())


    df_NPV['fee_amt_corr'] = df_NPV['fee_amt_x'].loc[range(-3,0)].mean() - df_NPV['fee_amt_y'].loc[range(-3,0)].mean()
    df_NPV['fee_amt_delta'] = df_NPV['fee_amt_x'] - df_NPV['fee_amt_y'] - df_NPV['fee_amt_corr']
    df_NPV.loc[0,'fee_amt_delta'] = 0
    df_NPV['fee_amt_delta'] = df_NPV['fee_amt_delta'].fillna(df_NPV['fee_amt_delta'].loc[range(4,7)].mean())

    df_NPV['income_before_tax'] = df_NPV['summa_pokupki_delta'] + df_NPV['kd_payment_delta'] + df_NPV['fee_amt_delta'] 

    NPV,df_NPV = NPV_tail(df_NPV)
    return(NPV,df_NPV)

def NPV_199(df_tgg_full, df_ctg_full,periods,df_NPV_XX):
    df_tgg_NPV = df_tgg_full.groupby(['t']).mean().reset_index()
    df_ctg_NPV = df_ctg_full.groupby(['t']).mean().reset_index()
    df_NPV = df_tgg_NPV[['t','summa_pokupki','kd_payment']].merge(df_ctg_NPV[['t','summa_pokupki','kd_payment']], how = 'left', on = 't')
    df_NPV = df_NPV.set_index('t')
    
    df_NPV = df_NPV.reindex(df_NPV.index.union(range(df_NPV.index[-1],0 + periods)))
    df_NPV['life_month'] = range(0,len(df_NPV))
    df_NPV['summa_pokupki_delta'] = df_NPV['summa_pokupki_x'] - df_NPV['summa_pokupki_y']
    df_NPV['summa_pokupki_delta'] = df_NPV['summa_pokupki_delta'].fillna(df_NPV['summa_pokupki_delta'].loc[range(4,7)].mean())

    df_NPV['kd_payment_corr'] = df_NPV['kd_payment_x'].loc[range(-3,0)].mean() - df_NPV['kd_payment_y'].loc[range(-3,0)].mean()
    df_NPV['kd_payment_delta'] = df_NPV['kd_payment_x'] - df_NPV['kd_payment_y'] - df_NPV['kd_payment_corr']
    df_NPV.loc[0,'kd_payment_delta'] = 0
    df_NPV['kd_payment_delta'] = df_NPV['kd_payment_delta'].fillna(df_NPV['kd_payment_delta'].loc[range(4,7)].mean())

    df_NPV['income_before_tax'] = df_NPV['summa_pokupki_delta'] + df_NPV['kd_payment_delta']
    
    NPV,df_NPV = NPV_tail(df_NPV)
    return(NPV,df_NPV)

def NPV_499(df_tgg_full, df_ctg_full,periods,df_NPV_XX):
    df_tgg_NPV = df_tgg_full.groupby(['t']).mean().reset_index()
    df_ctg_NPV = df_ctg_full.groupby(['t']).mean().reset_index()
    df_NPV = df_tgg_NPV[['t','summa_pokupki','kd_payment']].merge(df_ctg_NPV[['t','summa_pokupki','kd_payment']], how = 'left', on = 't')
    df_NPV = df_NPV.set_index('t')
    
    df_NPV['1mth'] = df_NPV_XX['summa_pokupki_x']
    
    df_NPV = df_NPV.reindex(df_NPV.index.union(range(df_NPV.index[-1],0  +periods)))
    df_NPV['ind'] = df_NPV.index
    
    df_NPV['1mth'] = df_NPV['1mth'].fillna(df_NPV['1mth'].loc[range(4,7)].mean())
    df_NPV['prolongation'] = df_NPV['ind'] // 3

    for i in range(7,df_NPV.index[-1] + 1):
        if df_NPV.loc[i,'ind'] % 3 == 0:
            df_NPV.loc[i,'summa_pokupki_x'] = float(df_NPV.loc[df_NPV['ind'] == int(df_NPV.loc[i,'prolongation']),'1mth']) / float(df_NPV.loc[df_NPV['ind'] == int(df_NPV.loc[i,'prolongation']) - 1,'1mth']) * float(df_NPV.loc[i - 3,'summa_pokupki_x'])
        else:
            df_NPV.loc[i,'summa_pokupki_x'] = float(df_NPV.loc[i - 3,'summa_pokupki_x']) / float(df_NPV.loc[i - 3 - (i % 3),'summa_pokupki_x']) * float(df_NPV.loc[i - (i % 3),'summa_pokupki_x'])
    df_NPV['summa_pokupki_y']  = df_NPV['summa_pokupki_y'].fillna(df_NPV['summa_pokupki_y'].loc[range(4,7)].mean())
    
    df_NPV['summa_pokupki_delta'] = df_NPV['summa_pokupki_x'] - df_NPV['summa_pokupki_y'] 
    df_NPV['kd_payment_corr'] =  df_NPV['kd_payment_x'].loc[range(-3,0)].mean() - df_NPV['kd_payment_y'].loc[range(-3,0)].mean()
    
    df_NPV['kd_payment_good_x'] = 0
    df_NPV['kd_payment_good_y'] = 0
    
    df_NPV.loc[0,'kd_payment_good_x'] = df_NPV.loc[0,'kd_payment_x'] 
    df_NPV.loc[0,'kd_payment_good_y'] = df_NPV.loc[0,'kd_payment_y'] + df_NPV.loc[0,'kd_payment_corr']
    for i in range(1,7):
        if df_NPV.loc[i,'ind'] % 3 == 1:
            df_NPV.loc[i,'kd_payment_good_x'] = df_NPV['kd_payment_x'].loc[range(i,i + 3)].mean()
            df_NPV.loc[i,'kd_payment_good_y'] = df_NPV['kd_payment_y'].loc[range(i,i + 3)].mean() + df_NPV.loc[0,'kd_payment_corr']
        else:
            df_NPV.loc[i,'kd_payment_good_x'] = df_NPV.loc[i - 1,'kd_payment_good_x']
            df_NPV.loc[i,'kd_payment_good_y'] = df_NPV.loc[i - 1,'kd_payment_good_y']
            
    df_NPV['kd_payment_good_delta'] = df_NPV['kd_payment_good_x'] - df_NPV['kd_payment_good_y']
    df_NPV.loc[0,'kd_payment_good_delta'] = 0

    df_NPV['tech'] = 0
    for i in range(3,df_NPV.index[-1] + 1):
        df_NPV.loc[i,'tech'] = df_NPV.loc[df_NPV['prolongation'] == df_NPV.loc[i,'prolongation'],'summa_pokupki_delta'].mean()/df_NPV.loc[df_NPV['prolongation']==df_NPV.loc[i,'prolongation']-1,'summa_pokupki_delta'].mean()
    
    for i in range(7,df_NPV.index[-1] + 1):
        if df_NPV.loc[i,'ind'] % 3 == 1:
            df_NPV.loc[i,'kd_payment_good_delta'] = df_NPV.loc[i - 1,'kd_payment_good_delta'] * df_NPV.loc[i,'tech']
        else:
            df_NPV.loc[i,'kd_payment_good_delta'] = df_NPV.loc[i - 1,'kd_payment_good_delta']
            
    df_NPV['income_before_tax'] = df_NPV['summa_pokupki_delta'] + df_NPV['kd_payment_good_delta']
    
    NPV,df_NPV = NPV_tail(df_NPV)
    return(NPV,df_NPV)

def NPV_749(df_tgg_full, df_ctg_full,periods,df_NPV_XX):
    df_tgg_NPV = df_tgg_full.groupby(['t']).mean().reset_index()
    df_ctg_NPV = df_ctg_full.groupby(['t']).mean().reset_index()
    df_NPV = df_tgg_NPV[['t','summa_pokupki','kd_payment','fee_amt']].merge(df_ctg_NPV[['t','summa_pokupki','kd_payment','fee_amt']], how='left', on='t')
    df_NPV = df_NPV.set_index('t')
    
    df_NPV['1mth'] = df_NPV_XX['summa_pokupki_x']
    
    df_NPV = df_NPV.reindex(df_NPV.index.union(range(df_NPV.index[-1],0 + periods)))
    df_NPV['ind'] = df_NPV.index
    
    df_NPV['1mth'] = df_NPV['1mth'].fillna(df_NPV['1mth'].loc[range(4,7)].mean())
    df_NPV['prolongation'] = df_NPV['ind'] // 3

    for i in range(7,df_NPV.index[-1] + 1):
        if df_NPV.loc[i,'ind'] % 3 == 0:
            df_NPV.loc[i,'summa_pokupki_x'] = float(df_NPV.loc[df_NPV['ind'] == int(df_NPV.loc[i,'prolongation']),'1mth']) / float(df_NPV.loc[df_NPV['ind'] == int(df_NPV.loc[i,'prolongation']) - 1,'1mth']) * float(df_NPV.loc[i - 3,'summa_pokupki_x'])
        else:
            df_NPV.loc[i,'summa_pokupki_x'] = float(df_NPV.loc[i - 3,'summa_pokupki_x']) / float(df_NPV.loc[i - 3 - (i % 3),'summa_pokupki_x']) * float(df_NPV.loc[i - (i % 3),'summa_pokupki_x'])
    df_NPV['summa_pokupki_y']  = df_NPV['summa_pokupki_y'].fillna(df_NPV['summa_pokupki_y'].loc[range(4,7)].mean())
    
    df_NPV['summa_pokupki_delta'] = df_NPV['summa_pokupki_x'] - df_NPV['summa_pokupki_y'] 
    
    df_NPV['kd_payment_corr'] =  df_NPV['kd_payment_x'].loc[range(-3,0)].mean() - df_NPV['kd_payment_y'].loc[range(-3,0)].mean()
    
    df_NPV['kd_payment_good_x'] = 0
    df_NPV['kd_payment_good_y'] = 0
    
    df_NPV.loc[0,'kd_payment_good_x'] = df_NPV.loc[0,'kd_payment_x'] 
    df_NPV.loc[0,'kd_payment_good_y'] = df_NPV.loc[0,'kd_payment_y'] + df_NPV.loc[0,'kd_payment_corr']
    for i in range(1,7):
        if df_NPV.loc[i,'ind'] % 3 == 1:
            df_NPV.loc[i,'kd_payment_good_x'] = df_NPV['kd_payment_x'].loc[range(i,i + 3)].mean()
            df_NPV.loc[i,'kd_payment_good_y'] = df_NPV['kd_payment_y'].loc[range(i,i + 3)].mean() + df_NPV.loc[0,'kd_payment_corr']
        else:
            df_NPV.loc[i,'kd_payment_good_x'] = df_NPV.loc[i-1,'kd_payment_good_x']
            df_NPV.loc[i,'kd_payment_good_y'] = df_NPV.loc[i-1,'kd_payment_good_y']
            
    df_NPV['kd_payment_good_delta'] = df_NPV['kd_payment_good_x'] - df_NPV['kd_payment_good_y']
    df_NPV.loc[0,'kd_payment_good_delta'] = 0
    
    df_NPV['fee_amt_corr'] =  df_NPV['fee_amt_x'].loc[range(-3,0)].mean() - df_NPV['fee_amt_y'].loc[range(-3,0)].mean()
    
    df_NPV['fee_amt_good_x'] = 0
    df_NPV['fee_amt_good_y'] = 0
    
    df_NPV.loc[0,'fee_amt_good_x'] = df_NPV.loc[0,'fee_amt_x'] 
    df_NPV.loc[0,'fee_amt_good_y'] = df_NPV.loc[0,'fee_amt_y'] + df_NPV.loc[0,'fee_amt_corr']
    for i in range(1,7):
        if df_NPV.loc[i,'ind'] % 3 == 1:
            df_NPV.loc[i,'fee_amt_good_x'] = df_NPV['fee_amt_x'].loc[range(i,i + 3)].mean()
            df_NPV.loc[i,'fee_amt_good_y'] = df_NPV['fee_amt_y'].loc[range(i,i + 3)].mean() + df_NPV.loc[0,'fee_amt_corr']
        else:
            df_NPV.loc[i,'fee_amt_good_x'] = df_NPV.loc[i - 1,'fee_amt_good_x']
            df_NPV.loc[i,'fee_amt_good_y'] = df_NPV.loc[i - 1,'fee_amt_good_y']
            
    df_NPV['fee_amt_good_delta'] = df_NPV['fee_amt_good_x'] - df_NPV['fee_amt_good_y']
    df_NPV.loc[0,'fee_amt_good_delta'] = 0

    df_NPV['tech'] = 0
    for i in range(3,df_NPV.index[-1] + 1):
        df_NPV.loc[i,'tech'] = df_NPV.loc[df_NPV['prolongation'] == df_NPV.loc[i,'prolongation'],'summa_pokupki_delta'].mean()/df_NPV.loc[df_NPV['prolongation']==df_NPV.loc[i,'prolongation']-1,'summa_pokupki_delta'].mean()
    
    for i in range(7,df_NPV.index[-1] + 1):
        if df_NPV.loc[i,'ind'] % 3 == 1:
            df_NPV.loc[i,'kd_payment_good_delta'] = df_NPV.loc[i - 1,'kd_payment_good_delta'] * df_NPV.loc[i,'tech']
            df_NPV.loc[i,'fee_amt_good_delta'] = df_NPV.loc[i - 1,'fee_amt_good_delta'] * df_NPV.loc[i,'tech']
        else:
            df_NPV.loc[i,'kd_payment_good_delta'] = df_NPV.loc[i - 1,'kd_payment_good_delta']
            df_NPV.loc[i,'fee_amt_good_delta'] = df_NPV.loc[i - 1,'fee_amt_good_delta']
            
    df_NPV['income_before_tax'] = df_NPV['summa_pokupki_delta'] + df_NPV['kd_payment_good_delta'] + df_NPV['fee_amt_good_delta'] 
    
    NPV,df_NPV = NPV_tail(df_NPV)
    return(NPV,df_NPV)

def NPV_1599(df_tgg_full, df_ctg_full,periods,df_NPV_XX):
    df_tgg_NPV = df_tgg_full.groupby(['t']).mean().reset_index()
    df_ctg_NPV = df_ctg_full.groupby(['t']).mean().reset_index()
    df_NPV = df_tgg_NPV[['t','summa_pokupki','kd_payment']].merge(df_ctg_NPV[['t','summa_pokupki','kd_payment']], how = 'left', on = 't')
    df_NPV = df_NPV.set_index('t')

    df_NPV = df_NPV.reindex(df_NPV.index.union(range(df_NPV.index[-1],0 + periods)))
    df_NPV['ind'] = df_NPV.index
    df_NPV['prolongation'] = df_NPV['ind'] // 12

    df_NPV['3mth'] = df_NPV_XX['summa_pokupki_x']

    for i in range(7,df_NPV.index[-1] + 1):
        if df_NPV.loc[i,'ind'] % 12 == 0:
            df_NPV.loc[i,'summa_pokupki_x'] = df_NPV.loc[i - 12,'summa_pokupki_x'] / df_NPV.loc[(df_NPV.loc[i,'prolongation'] - 1) * 3,'3mth'] * df_NPV.loc[(df_NPV.loc[i,'prolongation']) * 3,'3mth']
        else:
            if df_NPV.loc[i - 12 - (i % 12),'summa_pokupki_x'] == 0:
                df_NPV.loc[i,'summa_pokupki_x'] = 0
            else:
                df_NPV.loc[i,'summa_pokupki_x'] = float(df_NPV.loc[i - 12,'summa_pokupki_x']) / float(df_NPV.loc[i - 12 - (i % 12),'summa_pokupki_x']) * float(df_NPV.loc[i - (i % 12),'summa_pokupki_x'])

    df_NPV['summa_pokupki_y']  = df_NPV['summa_pokupki_y'].fillna(df_NPV['summa_pokupki_y'].loc[range(4,7)].mean())

    df_NPV['summa_pokupki_delta'] = df_NPV['summa_pokupki_x'] - df_NPV['summa_pokupki_y'] 

    df_NPV['kd_payment_corr'] =  df_NPV['kd_payment_x'].loc[range(-3,0)].mean() - df_NPV['kd_payment_y'].loc[range(-3,0)].mean()

    df_NPV['kd_payment_good_x'] = 0
    df_NPV['kd_payment_good_y'] = 0

    df_NPV.loc[0,'kd_payment_good_x'] = df_NPV.loc[0,'kd_payment_x'] 
    df_NPV.loc[0,'kd_payment_good_y'] = df_NPV.loc[0,'kd_payment_y'] + df_NPV.loc[0,'kd_payment_corr']

    for i in range(1,7):
        if df_NPV.loc[i,'ind'] % 3 == 1:
            df_NPV.loc[i,'kd_payment_good_x'] = df_NPV['kd_payment_x'].loc[range(i,i + 3)].mean()
            df_NPV.loc[i,'kd_payment_good_y'] = df_NPV['kd_payment_y'].loc[range(i,i + 3)].mean() + df_NPV.loc[0,'kd_payment_corr']
        else:
            df_NPV.loc[i,'kd_payment_good_x'] = df_NPV.loc[i - 1,'kd_payment_good_x']
            df_NPV.loc[i,'kd_payment_good_y'] = df_NPV.loc[i- 1,'kd_payment_good_y']

    df_NPV['kd_payment_good_delta'] = df_NPV['kd_payment_good_x'] - df_NPV['kd_payment_good_y']
    df_NPV.loc[0,'kd_payment_good_delta'] = 0

    df_NPV['tech'] = 0
    for i in range(13,df_NPV.index[-1] + 1):
        df_NPV.loc[i,'tech'] = df_NPV.loc[df_NPV['prolongation'] == df_NPV.loc[i,'prolongation'],'summa_pokupki_delta'].mean() / df_NPV.loc[df_NPV['prolongation'] == df_NPV.loc[i,'prolongation'] - 1,'summa_pokupki_delta'].mean()

    for i in range(7,df_NPV.index[-1] + 1):
        if df_NPV.loc[i,'ind'] % 12 == 1:
            df_NPV.loc[i,'kd_payment_good_delta'] = df_NPV.loc[i - 1,'kd_payment_good_delta'] * df_NPV.loc[i,'tech']
        else:
            df_NPV.loc[i,'kd_payment_good_delta'] = df_NPV.loc[i - 1,'kd_payment_good_delta']

    df_NPV['income_before_tax'] = df_NPV['summa_pokupki_delta'] + df_NPV['kd_payment_good_delta']  

    NPV,df_NPV = NPV_tail(df_NPV)
    return(NPV,df_NPV)

def NPV_2499(df_tgg_full, df_ctg_full,periods,df_NPV_XX):
    df_tgg_NPV = df_tgg_full.groupby(['t']).mean().reset_index()
    df_ctg_NPV = df_ctg_full.groupby(['t']).mean().reset_index()
    df_NPV = df_tgg_NPV[['t','summa_pokupki','kd_payment','fee_amt']].merge(df_ctg_NPV[['t','summa_pokupki','kd_payment','fee_amt']], how='left', on='t')
    df_NPV = df_NPV.set_index('t')

    df_NPV = df_NPV.reindex(df_NPV.index.union(range(df_NPV.index[-1],0 + periods)))
    df_NPV['ind'] = df_NPV.index
    df_NPV['prolongation'] = df_NPV['ind'] // 12

    df_NPV['3mth'] = df_NPV_XX['summa_pokupki_x']

    for i in range(7,df_NPV.index[-1] + 1):
        if df_NPV.loc[i,'ind'] % 12 == 0:
            df_NPV.loc[i,'summa_pokupki_x'] = df_NPV.loc[i - 12,'summa_pokupki_x'] / df_NPV.loc[(df_NPV.loc[i,'prolongation'] - 1) * 3,'3mth'] * df_NPV.loc[(df_NPV.loc[i,'prolongation']) * 3,'3mth']
        else:
            if df_NPV.loc[i - 12 - (i % 12),'summa_pokupki_x'] == 0:
                df_NPV.loc[i,'summa_pokupki_x'] = 0
            else:
                df_NPV.loc[i,'summa_pokupki_x'] = float(df_NPV.loc[i - 12,'summa_pokupki_x']) / float(df_NPV.loc[i - 12 - (i % 12),'summa_pokupki_x']) * float(df_NPV.loc[i - (i % 12),'summa_pokupki_x'])

    df_NPV['summa_pokupki_y']  = df_NPV['summa_pokupki_y'].fillna(df_NPV['summa_pokupki_y'].loc[range(4,7)].mean())

    df_NPV['summa_pokupki_delta'] = df_NPV['summa_pokupki_x'] - df_NPV['summa_pokupki_y'] 

    df_NPV['kd_payment_corr'] =  df_NPV['kd_payment_x'].loc[range(-3,0)].mean() - df_NPV['kd_payment_y'].loc[range(-3,0)].mean()

    df_NPV['kd_payment_good_x'] = 0
    df_NPV['kd_payment_good_y'] = 0

    df_NPV.loc[0,'kd_payment_good_x'] = df_NPV.loc[0,'kd_payment_x'] 
    df_NPV.loc[0,'kd_payment_good_y'] = df_NPV.loc[0,'kd_payment_y'] + df_NPV.loc[0,'kd_payment_corr']

    for i in range(1,7):
        if df_NPV.loc[i,'ind'] % 3 == 1:
            df_NPV.loc[i,'kd_payment_good_x'] = df_NPV['kd_payment_x'].loc[range(i,i + 3)].mean()
            df_NPV.loc[i,'kd_payment_good_y'] = df_NPV['kd_payment_y'].loc[range(i,i + 3)].mean() + df_NPV.loc[0,'kd_payment_corr']
        else:
            df_NPV.loc[i,'kd_payment_good_x'] = df_NPV.loc[i - 1,'kd_payment_good_x']
            df_NPV.loc[i,'kd_payment_good_y'] = df_NPV.loc[i - 1,'kd_payment_good_y']

    df_NPV['kd_payment_good_delta'] = df_NPV['kd_payment_good_x'] - df_NPV['kd_payment_good_y']
    df_NPV.loc[0,'kd_payment_good_delta'] = 0

    df_NPV['fee_amt_corr'] =  df_NPV['fee_amt_x'].loc[range(-3,0)].mean() - df_NPV['fee_amt_y'].loc[range(-3,0)].mean()

    df_NPV['fee_amt_good_x'] = 0
    df_NPV['fee_amt_good_y'] = 0

    df_NPV.loc[0,'fee_amt_good_x'] = df_NPV.loc[0,'fee_amt_x'] 
    df_NPV.loc[0,'fee_amt_good_y'] = df_NPV.loc[0,'fee_amt_y'] + df_NPV.loc[0,'fee_amt_corr']

    for i in range(1,7):
        if df_NPV.loc[i,'ind'] % 3 == 1:
            df_NPV.loc[i,'fee_amt_good_x'] = df_NPV['fee_amt_x'].loc[range(i,i + 3)].mean()
            df_NPV.loc[i,'fee_amt_good_y'] = df_NPV['fee_amt_y'].loc[range(i,i + 3)].mean() + df_NPV.loc[0,'fee_amt_corr']
        else:
            df_NPV.loc[i,'fee_amt_good_x'] = df_NPV.loc[i - 1,'fee_amt_good_x']
            df_NPV.loc[i,'fee_amt_good_y'] = df_NPV.loc[i - 1,'fee_amt_good_y']

    df_NPV['fee_amt_good_delta'] = df_NPV['fee_amt_good_x'] - df_NPV['fee_amt_good_y']
    df_NPV.loc[0,'fee_amt_good_delta'] = 0
    
    df_NPV['tech'] = 0
    for i in range(13,df_NPV.index[-1] + 1):
        df_NPV.loc[i,'tech'] = df_NPV.loc[df_NPV['prolongation'] == df_NPV.loc[i,'prolongation'],'summa_pokupki_delta'].mean() / df_NPV.loc[df_NPV['prolongation'] == df_NPV.loc[i,'prolongation'] - 1,'summa_pokupki_delta'].mean()

    for i in range(7,df_NPV.index[-1] + 1):
        if df_NPV.loc[i,'ind'] % 12 == 1:
            df_NPV.loc[i,'kd_payment_good_delta'] = df_NPV.loc[i - 1,'kd_payment_good_delta'] * df_NPV.loc[i,'tech']
            df_NPV.loc[i,'fee_amt_good_delta'] = df_NPV.loc[i - 1,'fee_amt_good_delta'] * df_NPV.loc[i,'tech']
        else:
            df_NPV.loc[i,'kd_payment_good_delta'] = df_NPV.loc[i - 1,'kd_payment_good_delta']
            df_NPV.loc[i,'fee_amt_good_delta'] = df_NPV.loc[i - 1,'fee_amt_good_delta']

    df_NPV['income_before_tax'] = df_NPV['summa_pokupki_delta'] + df_NPV['kd_payment_good_delta'] + df_NPV['fee_amt_good_delta']  

    NPV,df_NPV = NPV_tail(df_NPV)
    return(NPV,df_NPV)
