import pandas as pd
import sqlite3
import numpy as np

conn = sqlite3.connect('brasileirao_predict.db')

comando = """
SELECT 
p.*, 
c.temperatura,
c.chuva,
c.condicao
FROM partidas p 
LEFT JOIN clima c
    ON p.data = c.data AND p.cidade = c.cidade
"""

df_master = pd.read_sql(comando, conn)

df_master = df_master.drop_duplicates()

conn.close()

def calcula_pontos(linha, time):
    if linha['mandante'] == time and linha['resultado'] == 'H' or linha ['visitante'] == time and linha['resultado'] == 'A':
        return 3
    elif linha['mandante'] == time and linha['resultado'] == 'A' or linha ['visitante'] == time and linha['resultado'] == 'H':
        return 0
    else:
        return 1

lista_processada = []

lista_times = df_master['mandante'].drop_duplicates()

for time in lista_times:
    df_jogos_time = df_master[(df_master['mandante'] == time) | (df_master['visitante'] == time)].copy()
    
    df_jogos_time = df_jogos_time.sort_values('data')
    
    df_jogos_time['pontos'] = df_jogos_time.apply(lambda row: calcula_pontos(row, time), axis = 1)
    
    df_jogos_time['ultimos_5'] = df_jogos_time['pontos'].shift(1).rolling(window=5, min_periods = 1).sum()
    
    df_jogos_time['gols_pro'] = np.where(df_jogos_time['mandante'] == time, df_jogos_time['gols_mandante'], df_jogos_time['gols_visitante'])
    
    df_jogos_time['gols_contra'] = np.where(df_jogos_time['mandante'] == time, df_jogos_time['gols_visitante'], df_jogos_time['gols_mandante'])
    
    df_jogos_time['media_gols_pro'] = df_jogos_time['gols_pro'].shift(1).rolling(window=5, min_periods = 1).mean()
    
    df_jogos_time['media_gols_contra'] = df_jogos_time['gols_contra'].shift(1).rolling(window=5, min_periods = 1).mean()
    
    df = pd.DataFrame({
        'data': df_jogos_time['data'],
        'time': time,
        'ultimos_5': df_jogos_time['ultimos_5'],
        'media_gols_pro': df_jogos_time['media_gols_pro'],
        'media_gols_contra': df_jogos_time['media_gols_contra']
        })
    
    lista_processada.append(df)

df_hist = pd.concat(lista_processada)

df_master = pd.merge(
    df_master,
    df_hist, 
    left_on = ['data', 'mandante'],
    right_on = ['data', 'time'],
    how = 'left'
)

df_master = df_master.rename(columns={'ultimos_5': 'mandante_ult_5', 'media_gols_pro': 'media_gols_pro_mandante', 'media_gols_contra': 'media_gols_contra_mandante'})
df_master = df_master.drop(columns=['time'])

df_master = pd.merge(
    df_master, 
    df_hist, 
    left_on=['data', 'visitante'], 
    right_on=['data', 'time'], 
    how='left'
)
df_master = df_master.rename(columns={'ultimos_5': 'visitante_ult_5', 'media_gols_pro': 'media_gols_pro_visitante', 'media_gols_contra': 'media_gols_contra_visitante'})
df_master = df_master.drop(columns=['time'])
df_master = df_master.fillna(0)

df_master = df_master.drop(columns=['gols_visitante', 'gols_mandante', 'cidade'])
df_master_final = pd.get_dummies(df_master, columns=['condicao'], dtype=int)

conn = sqlite3.connect('tb_modelagem.db')
df_master_final.to_sql('model_input', conn, if_exists='replace', index=False)

conn.close()