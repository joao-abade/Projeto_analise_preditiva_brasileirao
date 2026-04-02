import sqlite3
import time

from src.ingestion.weather_api import buscar_clima

cidades_times = {
    "Palmeiras" : "São Paulo",
    "Corinthians": "São Paulo",
    "São Paulo": "São Paulo",
    "Santos": "Santos",
    "Flamengo": "Rio de Janeiro",
    "Fluminense": "Rio de Janeiro",
    "Vasco": "Rio de Janeiro",
    "Botafogo": "Rio de Janeiro",
    "Cruzeiro": "Belo Horizonte",
    "Atlético Mineiro": "Belo Horizonte",
    "América Mineiro": "Belo Horizonte",
    "Grêmio": "Porto Alegre",
    "Internacional": "Porto Alegre",
    "Juventude": "Caxias do Sul",
    "Athletico Paranaense": "Curitiba",
    "Coritiba": "Curitiba",
    "Bahia": "Salvador",
    "Vitória": "Salvador",
    "Cuiaba": "Cuiaba",
    "Sport": "Recife",
    "Fortaleza": "Fortaleza",
    "Ceará": "Fortaleza",
}

def atualizar_clima_no_banco():
    conn = sqlite3.connect('../../brasileirao_predict.db')
    cursor = conn.sursor()
    
    cursor.execute(''' SELECT id, data, mandante
                   FROM partidas_raw
                   WHERE clima_temp IS NULL''')
    
    jogos_sem_clima = cursor.fetchall()
    print(f"Encontrados {len(jogos_sem_clima)} jogos precisando de dados climáticos")
    
    for jogo in jogos_sem_clima:
        jogo_id = jogo[0]
        data_jogo = jogo[1]
        time_mandante = jogo[2]
        
        cidade = cidades_times.get(time_mandante)
        
        if cidade:
            try:
                print(f'Buscando clima para {time_mandante} em {cidade} na data {data_jogo}')
                
                temp, chuva, condicao = buscar_clima(cidade, data_jogo)
                
                cursor.execute(''' UPDATE partidas_raw
                               SET clima_temp = ?, precip_mm = ?, clica_condicao = ?
                               WHERE id= ?
                               ''', (temp, chuva, condicao, jogo_id))
                
                conn.comit()
                
                time.sleep(2)
                
            except  Exception as e:
                print(f"Erro ao buscar clima para o ID{jogo_id}: {e}")
        else:
            print(f"Cidade não mapeada para o time: {time_mandante}")
               
        
    conn.close()
