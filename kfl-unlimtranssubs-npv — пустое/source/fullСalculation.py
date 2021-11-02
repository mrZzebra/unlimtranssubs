import pandas as pd
from source.preprocessing import preprocessing_1_SDO
from source.preprocessing import preprocessing_2_cards
from source.preprocessing import preprocessing_3_pmt
from source.preprocessing import preprocessing_4_subscr
from source.preprocessing import preprocessing_5_assembling
from source.preprocessing import preprocessing_6_drop_sber1nPB
import source.splitting as splt
from source.matching import matching
import source.NPV as npv
import json

def full_calculation(starting_vintage,periods, mid):
    result = {}
    result['id'] = mid
    
    df_res = pd.DataFrame(columns=['subscription_type','NPV'])
    
    df_tgg_SDO = preprocessing_1_SDO('support/data/df_cg_1.txt')
    df_ctg_SDO = preprocessing_1_SDO('support/data/df_kg_1.txt')
    
    df_tgg_card = preprocessing_2_cards('support/data/df_cg_2.txt')
    df_ctg_card = preprocessing_2_cards('support/data/df_kg_2.txt')
    
    pay_cg = preprocessing_3_pmt('support/data/pay_cg.txt')
    pay_kg = preprocessing_3_pmt('support/data/pay_kg.txt')
    
    df_SUBS_first,df_SUBS_sumbymonth = preprocessing_4_subscr('support/data/SUBS_sample.txt')
    
    df_tgg = preprocessing_5_assembling(df_tgg_card,df_tgg_SDO,df_SUBS_first,df_SUBS_sumbymonth,pay_cg)
    df_ctg = preprocessing_5_assembling(df_ctg_card,df_ctg_SDO,df_SUBS_first,df_SUBS_sumbymonth,pay_kg)
    
    df_tgg = preprocessing_6_drop_sber1nPB(df_tgg,'support/data/SQLAExport.txt')
    df_ctg = preprocessing_6_drop_sber1nPB(df_ctg,'support/data/SQLAExport.txt')

    NPV_dict = {199:npv.NPV_199,499:npv.NPV_499,1599:npv.NPV_1599,299:npv.NPV_299,749:npv.NPV_749,2499:npv.NPV_2499}
    df_NPV_XX = pd.DataFrame()
    
    for tip in NPV_dict.keys():   
        CG_type = splt.choose(df_tgg,tip)

        CG_full,KG_full,list_cg,list_kg,list_cl,mnths = matching (CG_type, df_ctg,tip,starting_vintage=starting_vintage)

        NPV,df_NPV_XX = NPV_dict.get(tip)(CG_full, KG_full, periods, df_NPV_XX)
        df_res = df_res.append({'subscription_type':tip,'NPV':NPV},ignore_index=True)
        
    result['output'] = json.loads(df_res.to_json(orient='records'))    
    return(result)