import pandas as pd
import dask.dataframe as dd

def valida_cpf(cpf):
    cpf = str(cpf)
    if len(cpf)!= 11:
        return False
    if not cpf.isdigit():
        return False
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = (soma * 10) % 11
    if resto == 10 or resto == 11:
        resto = 0
    if resto!= int(cpf[9]):
        return False
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = (soma * 10) % 11
    if resto == 10 or resto == 11:
        resto = 0
    if resto!= int(cpf[10]):
        return False
    return True

def valida_cpf_batch(df):
    df['CPF_VALIDO'] = df['CPF'].apply(valida_cpf)
    df_validado = df[df['CPF_VALIDO']]
    df_validado = df_validado.drop_duplicates(subset='CPF')
    return df_validado

df = pd.read_excel('CLARO _21_filtrado.xlsx', na_values=['', 'NA', 'nan'])
print(df.columns)
df = df.dropna(subset=['CPF'])

ddf = dd.from_pandas(df, npartitions=4)

ddf_validado = ddf.map_partitions(valida_cpf_batch).compute()

cpf_invalidos_count = len(df) - len(ddf_validado)
print(f"Número total de CPFs inválidos ou duplicados: {cpf_invalidos_count}")

ddf_validado = ddf_validado.drop_duplicates(subset='CPF')

cpf_invalidos_count = len(ddf_validado) - len(ddf_validado[ddf_validado['CPF_VALIDO']])
print(f"Número total de CPFs inválidos na segunda verificação: {cpf_invalidos_count}")

print("\nPlanilha após a segunda validação e filtragem:")
print(ddf_validado[ddf_validado['CPF_VALIDO']])

ddf_validado = ddf_validado[ddf_validado['CPF_VALIDO']]
ddf_validado.to_excel('test1_filtrado.xlsx', index=False, engine='openpyxl')