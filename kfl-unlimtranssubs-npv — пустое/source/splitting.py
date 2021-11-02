exclude_dic = {'299':['99.67','199.33'],'749':['249.67','499.33'], '2499':['1666','833']}
def choose(df_tgg, tip):

    df_first_buy = df_tgg[df_tgg['MonthsRD'] == df_tgg['MonthsSov_x']]
    client_tid_list = list(df_first_buy[df_first_buy[str(tip)]>0]['client_tid'])

    df_tgg = df_tgg[df_tgg['client_tid'].isin(client_tid_list)]

    if str(tip) in ['299', '749', '2499']:
        exclude = set(df_tgg[(df_tgg[exclude_dic[str(tip)][0]] > 0) | (df_tgg[exclude_dic[str(tip)][1]] > 0)].client_tid)
        df_tgg = df_tgg[df_tgg['client_tid'].isin(exclude) == False]
    return (df_tgg)