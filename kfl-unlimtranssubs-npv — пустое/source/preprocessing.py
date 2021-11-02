import pandas as pd
import source.support as spt
import source.dictionaries as dct

def preprocessing_1_SDO(path_to_file,sep = '\t',dec = '.'):
    df_SDO = pd.read_csv(path_to_file, sep = '\t',decimal = '.',encoding = 'utf-8',
        usecols = ['report_dt', 'Age', 'gender_cd', 'Client_tid', 'FullName', 'SDORur','segment_id_current',
       'is_payroll', 'is_employee', 'is_pensioner', 'is_resident','OSB_actual', 'GOSB_NUMBER'],dtype = {'Client_tid':'str',
        'SDORur':'float'})
    if 'Client_tid' in df_SDO.columns:
        df_SDO.rename(columns = {'Client_tid':'client_tid'}, inplace=True)

    df_SDO = df_SDO[df_SDO['Age'].isna() == False]

    df_SDO['MonthsRD'] = spt.count_months(df_SDO['report_dt'])

    indexes_to_drop = df_SDO.loc[df_SDO['FullName'].isin(dct.lst_drop)].index.tolist()
    indexes_to_keep = set(range(df_SDO.shape[0])) - set(indexes_to_drop)
    df_SDO = df_SDO.take(list(indexes_to_keep))

    df_SDO['SDORur'] = df_SDO['SDORur'].mask(df_SDO['SDORur']  <0,0)

    df_SDO['sohran'] = df_SDO['FullName'].isin(dct.lst_sohr)
    df_SDO['popoln'] = df_SDO['FullName'].isin(dct.lst_pop)
    df_SDO['upravl'] = df_SDO['FullName'].isin(dct.lst_upr)
    df_SDO['card'] = df_SDO['FullName'].isin(dct.lst_card)
    df_SDO['promo'] = df_SDO['FullName'].isin(dct.lst_promo)

    df_SDO['1']=1
    df_SDO['curr'] = df_SDO['1'] - (df_SDO['sohran'] + df_SDO['popoln'] + df_SDO['upravl'] + df_SDO['card'] + df_SDO['promo'])

    for item in ['sohran', 'popoln', 'upravl', 'card', 'promo', 'curr']:
        df_SDO[item] = df_SDO[item]*df_SDO['SDORur']

    df_SDO['gender_cd'].replace(['?','M', 'F'],[0, 1, 2], inplace = True)

    df_SDO.gender_cd = df_SDO.gender_cd.astype(int)
    df_SDO['Age'] = df_SDO['Age'].astype('int')

    df_SDO_stage1 = df_SDO.groupby(['client_tid','MonthsRD']).agg({'report_dt':'first','Age':'first','gender_cd':'first',
                                                    'is_employee':'first', 'is_pensioner':'first',
                                                    'segment_id_current':'last','GOSB_NUMBER':'first','OSB_actual':'first',
                                                       'sohran':'sum', 'popoln':'sum', 'upravl':'sum', 'card':'sum',
                                                       'promo':'sum', 'curr':'sum','SDORur':'sum'}).reset_index()
    
    df_SDO_stage2 = df_SDO_stage1.pivot_table(['card'], ['client_tid'], 'MonthsRD').reset_index()
    df_SDO_stage2 = pd.melt(df_SDO_stage2, id_vars = ['client_tid'])
    df_SDO_stage3 = df_SDO_stage2.merge(df_SDO_stage1, how ='left',left_on = ['client_tid','MonthsRD'], right_on = ['client_tid','MonthsRD'])

    df_forcols = df_SDO_stage3.head().select_dtypes(include = ['int','float'])
    list_cols = list(df_forcols.columns)
    for col in list_cols:
        df_SDO_stage3[col] = df_SDO_stage3[col].fillna(0)

    df_segments = df_SDO.groupby('client_tid').agg({'segment_id_current':'last'}).reset_index()
    df_segments['segm'] = 0
    df_segments['segm'] = df_segments['segm'].mask(df_segments['segment_id_current'].isin([11, 12, 13, 14, 15, 16]),'MASS')
    df_segments['segm'] = df_segments['segm'].mask(df_segments['segment_id_current'].isin([17, 18, 19, 20, 21, 22]),'MVS LIGHT')
    df_segments['segm'] = df_segments['segm'].mask(df_segments['segment_id_current'].isin([23, 24, 25, 26, 27, 28]),'MVS UPPER')
    df_segments['segm'] = df_segments['segm'].mask(df_segments['segment_id_current'].isin([29, 30, 31, 32, 33, 34]),'VIP')
    df_segments['segm'] = df_segments['segm'].mask(df_segments['segment_id_current'].isin([35, 36, 37, 38, 39, 40]),'PB')

    df_SDO_stage3 = df_SDO_stage3.merge(df_segments, how='left', left_on='client_tid', right_on='client_tid')    
    df_SDO_stage3 = pd.get_dummies(df_SDO_stage3,columns = ['segm'],drop_first=False)

    return(df_SDO_stage3)

def preprocessing_2_cards(path_to_file,sep = '\t',dec = '.'):
    df_cards = pd.read_csv(path_to_file, sep = sep,decimal=dec,encoding = 'utf-8',usecols = ['report_dt','client_tid','payment_sbol_inside',
                'kd_payment_sbol_inside','agrmnt_id','host_client_id'], dtype = {'client_tid':'str'})

    df_forcols = df_cards.head().select_dtypes(include = ['int','float'])
    list_cols = list(df_forcols.columns)
    for col in list_cols:
        df_cards[col] = df_cards[col].fillna(0)

    for col in list_cols:
        df_cards[col] = spt.mask_0(df_cards[col])

    df_cards['MonthsRD'] = spt.count_months(df_cards['report_dt'])

    df_cards['payment'] = df_cards['payment_sbol_inside']
    df_cards['kd_payment'] = df_cards['kd_payment_sbol_inside']

    df_cards = df_cards[['report_dt','agrmnt_id','client_tid',
           'host_client_id','payment',
           'kd_payment', 'MonthsRD']]

    df_cards_stage1 = df_cards.groupby(['client_tid','MonthsRD']).agg({'report_dt':'first','agrmnt_id':'first',
           'host_client_id':'first','payment':'sum',
           'kd_payment':'sum'}).reset_index()

    df_cards_stage2 = df_cards_stage1.pivot_table(['payment'], ['client_tid'], 'MonthsRD').reset_index()
    df_cards_stage2 = pd.melt(df_cards_stage2, id_vars=['client_tid'])
    df_cards_stage3 = df_cards_stage2.merge(df_cards_stage1, how = 'left',left_on = ['client_tid','MonthsRD'], right_on = ['client_tid','MonthsRD'])

    df_forcols = df_cards_stage3.head().select_dtypes(include = ['int','float'])
    list_cols = list(df_forcols.columns)
    for col in list_cols:
        df_cards_stage3[col] = df_cards_stage3[col].fillna(0)

    return(df_cards_stage3)

def preprocessing_3_pmt(df_pay):
    df_pay = pd.read_csv(df_pay,sep = '\t',usecols = ['report_dt','client_tid','pmt_amt','fee_amt'], dtype = {'client_tid':'str'})
    df_pay['MonthsRD'] = spt.count_months(df_pay['report_dt'])
    df_pay.pmt_amt = df_pay.pmt_amt.str.replace('?','0')
    df_pay.pmt_amt = df_pay.pmt_amt.astype('float')
    df_pay = df_pay.groupby(['client_tid','MonthsRD']).agg({'pmt_amt':'sum','fee_amt':'sum'}).reset_index()
    return(df_pay)

def preprocessing_4_subscr(df_SUBS):
    df_SUBS = pd.read_csv(df_SUBS, sep = '\t', encoding = 'utf-8',usecols = ['months_sovershenie','epk_id','summa_pokupki','C_COMMENT'])

    df_SUBS['MonthsSov'] = spt.count_months(df_SUBS['months_sovershenie'])
    df_SUBS = df_SUBS[df_SUBS['epk_id'].isna() == False]
    df_SUBS = df_SUBS[df_SUBS['epk_id'] != '?']
    df_SUBS = df_SUBS[df_SUBS['epk_id'] != '-1']

    df_SUBS.epk_id = df_SUBS.epk_id.astype('str')
    df_SUBS_first = df_SUBS.groupby('epk_id').agg({'MonthsSov':'min','summa_pokupki':'first','C_COMMENT':'first'}).reset_index()

    df_SUBS_sumbymonth = df_SUBS.groupby(['epk_id','MonthsSov']).sum().reset_index()
    
    df_SUBS_first['epk_id'] = df_SUBS_first['epk_id'].astype('str')
    df_SUBS_sumbymonth['epk_id'] = df_SUBS_sumbymonth['epk_id'].astype('str')
    
    return(df_SUBS_first,df_SUBS_sumbymonth)

def preprocessing_5_assembling(df_card,df_SDO,df_SUBS_first,df_SUBS_sumbymonth,df_pay):
    df_card = df_SDO.merge(df_card, how = 'inner', on = ['client_tid','MonthsRD'])
    
    del df_SDO
    
    df_card['client_tid'] = df_card['client_tid'].astype('str')

    df_subs_half = df_card.merge(df_SUBS_first, how = 'left', left_on = ['client_tid'], right_on = ['epk_id'])
    
    df_subs_full = df_subs_half.merge(df_SUBS_sumbymonth, how = 'left', left_on = ['client_tid','MonthsRD'], right_on = ['epk_id','MonthsSov'])
    df_subs_full.summa_pokupki_y = df_subs_full.summa_pokupki_y.fillna(0)
    df_subs_full = df_subs_full.rename(columns = {'summa_pokupki_x':'summa_pokupki_old','summa_pokupki_y':'summa_pokupki'})
    
    df_this_group = spt.spread_comission(df_subs_full)
    df_this_group = df_this_group.merge(df_pay, how = 'left',on = ['client_tid','MonthsRD'])
    df_this_group['SDO_sum'] = df_this_group['curr'] + df_this_group['card'] + df_this_group['promo'] + df_this_group['sohran']+df_this_group['popoln']+df_this_group['upravl']
    
    df_forcols = df_this_group.head().select_dtypes(include = ['int','float'])
    list_cols = list(df_forcols.columns)
    for col in list_cols:
        df_this_group[col] = df_this_group[col].fillna(0)
        df_this_group[col] = df_this_group[col].mask(df_this_group[col] < 0,0)

    #df_this_group['kd_sum_fight'] = df_this_group['summa_pokupki'] - df_this_group['kd_payment']  - df_this_group['fee_amt'] 
    #df_this_group['kd_sum'] = df_this_group['kd_payment'] + df_this_group['kd_payment_other_in'] + df_this_group['kd_payment_out'] + df_this_group['kd_withdraw'] + df_this_group['fee_amt'] + df_this_group['summa_pokupki']

    df_this_group['deposits'] = df_this_group['popoln'] + df_this_group['sohran'] + df_this_group['upravl'] + df_this_group['promo']

    df_this_group['has_it'] = 0
    df_this_group['has_it'] = df_this_group['has_it'].mask(df_this_group['sum_monthly'] > 0,1)

    return(df_this_group)

def preprocessing_6_drop_sber1nPB(df_this_group,channel):
    df_channel = pd.read_csv(channel, sep = '\t')
    df_this_group = df_this_group[df_this_group['client_tid'].isin(set(df_channel[df_channel['ChannelService'].isin([1,3])].Client_tid)) == False]
    return(df_this_group)
