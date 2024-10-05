import pandas as pd
import json
from create_collection import client

# Esse codigo faz a ingestao dos dados no mongoDB

#INGESTION

df_case = pd.read_csv('./model_training/data/train.csv')

#tratamento dos dados

#CONSUMPTION

new_df = pd.DataFrame(df_case.groupby('num_var4').mean()['TARGET'].sort_values(ascending = False))
new_df = new_df.reset_index().reset_index()
df_final_eng = new_df[['index', 'num_var4']].join(df_case.set_index('num_var4'), on= 'num_var4')#

df_final_eng.rename(columns = {'index':'var4_ordered'}, inplace = True)

features_zero =['num_var5_0',
'var4_ordered',
'var3',
'var15',
'imp_ent_var16_ult1',
'imp_op_var39_comer_ult1',
'imp_op_var39_comer_ult3',
'imp_op_var40_comer_ult1',
'imp_op_var40_comer_ult3',
'imp_op_var40_efect_ult1',
'imp_op_var40_efect_ult3',
'imp_op_var40_ult1',
'imp_op_var41_efect_ult1',
'imp_op_var41_efect_ult3',
'imp_op_var41_ult1',
'imp_sal_var16_ult1',
'ind_var1_0',
 'ind_var1',
 'ind_var2_0',
 'ind_var5_0',
 'ind_var5',
 'ind_var6_0',
 'ind_var6',
 'ind_var8_0',
 'ind_var8',
 'ind_var12_0',
 'ind_var12',
 'ind_var13_0',
 'ind_var13_corto_0',
 'ind_var13_largo_0',
 'ind_var13_medio_0',
 'ind_var14_0',
 'ind_var14',
 'ind_var17_0',
 'ind_var17',
 'ind_var18_0',
 'ind_var19',
 'ind_var20_0',
 'ind_var20',
 'ind_var24_0',
 'ind_var24',
 'ind_var25_cte',
 'ind_var26_0',
 'ind_var30_0',
 'ind_var30',
 'ind_var31_0',
 'ind_var31',
 'ind_var32_cte',
 'ind_var32_0',
 'ind_var33_0',
 'ind_var33',
 'ind_var34_0',
 'ind_var37_cte',
 'ind_var37_0',
 'ind_var39_0',
 'ind_var44_0',
 'ind_var44',
 'num_op_var40_hace2',
 'num_op_var40_hace3',
 'num_op_var41_hace2',
 'num_op_var41_hace3',
 'num_op_var41_ult3',
 'num_var30_0',
 'num_var30',
 'num_var37_med_ult2',
 'num_var39_0',
 'num_var42_0',
 'num_var42',
 'saldo_var5',
 'saldo_var30',
 'saldo_var42',
 'var36',
 'delta_imp_aport_var13_1y3',
 'delta_imp_aport_var17_1y3',
 'delta_imp_aport_var33_1y3',
 'delta_imp_compra_var44_1y3',
 'delta_imp_reemb_var13_1y3',
 'delta_imp_reemb_var17_1y3',
 'delta_imp_reemb_var33_1y3',
 'delta_imp_trasp_var17_in_1y3',
 'delta_imp_trasp_var17_out_1y3',
 'delta_imp_trasp_var33_in_1y3',
 'delta_imp_trasp_var33_out_1y3',
 'delta_imp_venta_var44_1y3',
 'delta_num_aport_var33_1y3',
 'delta_num_compra_var44_1y3',
 'imp_aport_var13_hace3',
 'imp_aport_var13_ult1',
 'imp_aport_var17_hace3',
 'imp_aport_var17_ult1',
 'imp_aport_var33_ult1',
 'imp_var7_emit_ult1',
 'imp_var7_recib_ult1',
 'imp_compra_var44_hace3',
 'imp_compra_var44_ult1',
 'imp_reemb_var17_hace3',
 'imp_var43_emit_ult1',
 'imp_trans_var37_ult1',
 'imp_trasp_var17_in_hace3',
 'imp_trasp_var17_in_ult1',
 'imp_trasp_var33_in_hace3',
 'imp_trasp_var33_in_ult1',
 'imp_venta_var44_hace3',
 'imp_venta_var44_ult1',
 'ind_var10_ult1',
 'ind_var10cte_ult1',
 'num_var22_hace2',
 'num_var22_hace3',
 'num_var22_ult1',
 'num_var22_ult3',
 'num_med_var22_ult3',
 'num_med_var45_ult3',
 'num_meses_var5_ult3',
 'num_meses_var13_largo_ult3',
 'num_meses_var17_ult3',
 'num_meses_var29_ult3',
 'num_meses_var39_vig_ult3',
 'num_trasp_var11_ult1',
 'num_var45_hace2',
 'num_var45_hace3',
 'num_var45_ult1',
 'num_var45_ult3',
 'saldo_medio_var5_hace2',
 'saldo_medio_var5_hace3',
 'saldo_medio_var8_hace2',
 'saldo_medio_var8_hace3',
 'saldo_medio_var12_hace2',
 'saldo_medio_var12_hace3',
 'saldo_medio_var13_corto_hace3',
 'saldo_medio_var13_largo_hace2',
 'saldo_medio_var13_largo_hace3',
 'saldo_medio_var17_hace2',
 'saldo_medio_var17_hace3',
 'saldo_medio_var29_hace2',
 'saldo_medio_var29_hace3',
 'saldo_medio_var29_ult1',
 'saldo_medio_var33_hace2',
 'saldo_medio_var33_hace3',
 'saldo_medio_var44_hace2',
 'var38',
]

df_final_eng['zero_info'] =(df_final_eng[features_zero] == 0).astype(int).sum(axis=1)

#BOOK OF FEATURES

features_finais = ['var4_ordered',
 'var15',
 'imp_op_var41_efect_ult1',
 'ind_var30',
 'ind_var39_0',
 'num_var30_0',
 'num_var30',
 'num_var39_0',
 'saldo_var30',
 'num_meses_var5_ult3',
 'num_var45_hace3',
 'num_var45_ult3',
 'zero_info',
'_id']

df_final_eng = df_final_eng.rename(columns={'ID': '_id'})


df_final = df_final_eng[features_finais]


#features ingestion

insert_data = df_final.to_json(orient='records')
features_details = json.loads(insert_data)

db = client['ML_db']
collection = db['credit_risk_features_input']

insert_doc = collection.insert_many(features_details)

client.close()