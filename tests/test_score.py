import pandas as pd
from app.main import get_model

def test_score():

    data = {"var4_ordered":0,"var15":44,"imp_op_var41_efect_ult1":0.0,"ind_var30":0,"ind_var39_0":0,"num_var30_0":3,"num_var30":0,"num_var39_0":0,"saldo_var30":0.0,"num_meses_var5_ult3":0,"num_var45_hace3":0,"num_var45_ult3":0,"zero_info":131}
    data2 = {"var4_ordered":0,"var15":23,"imp_op_var41_efect_ult1":0.0,"ind_var30":0,"ind_var39_0":1,"num_var30_0":3,"num_var30":0,"num_var39_0":3,"saldo_var30":0.0,"num_meses_var5_ult3":0,"num_var45_hace3":0,"num_var45_ult3":0,"zero_info":128}
    
    df = pd.DataFrame([data])
    df1 = pd.DataFrame([data2])

    assert get_model(df) == 1
    assert get_model(df1) == 0

