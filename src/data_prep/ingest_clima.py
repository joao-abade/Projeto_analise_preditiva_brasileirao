import sqlite3
import pandas as pd
from weather_api import buscar_clima
import time

conn = sqlite3.connect("brasileirao_predict.db")

df_locais = pd.read_sql("SELECT DISTINCT data, cidade FROM partidas WHERE cidade IS NOT NULL", conn)

lista_climas = []

for index, linha in df_locais.iterrows():
    data = linha['data']
    local = linha['cidade']
    
    temp, chuva, condicao = buscar_clima(local, data)
    
    dados_clima = {
        'data' : data,
        'cidade' : local,
        'temperatura' : temp,
        'chuva' : chuva,
        'condicao' : condicao 
    }
    
    lista_climas.append(dados_clima)
    
    time.sleep(1)
    
    
df_climas = pd.DataFrame(lista_climas)

df_climas.to_sql('clima', conn, if_exists = 'append', index=False)

conn.close()