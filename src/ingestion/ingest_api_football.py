import requests
import sqlite3
import pandas as pd

def ingest_temporada(ano):
    
    url = "https://v3.football.api-sports.io/fixtures"
    
    headers = {"x-apisports-key": "55a42df527da8bb2c84ecc51c16ac3f4"}
    
    params = {
        "league": "71", "season": str(ano)
    }
    
    resposta = requests.get(url, headers= headers, params= params)
    dados = resposta.json()
    
    jogos = dados.get('response', [])
    
    print(f"Total de jogos encontrados: {len(jogos)}")
    
    lista_banco = []
    
    for jogo in jogos:
        
        data = jogo["fixture"]["date"][:10]
        rodada = int(float(jogo["league"]["round"].split("-")[1]))
        mandante = jogo["teams"]["home"]["name"]
        visitante = jogo["teams"]["away"]["name"]
        
        if jogo['fixture']['status']['short'] == "FT":
            gols_mandante = int(float(jogo["goals"]["home"]))
            gols_visitante = int(float(jogo["goals"]["away"]))
            
            if gols_mandante > gols_visitante:
                resultado = "H"
            elif gols_visitante > gols_mandante:
                resultado = "A"
            else: resultado = "D"
            
        else:
            gols_mandante = None
            gols_visitante = None
            resultado = None
            
        cidade = jogo["fixture"]["venue"]["city"]
                
        dados_jogo = {
            'data' : data,
            'rodada' : rodada,
            'mandante' : mandante,
            'visitante' : visitante,
            "gols_mandante" : gols_mandante,
            'gols_visitante' : gols_visitante,
            'cidade' : cidade,
            'resultado' : resultado
        }

        lista_banco.append(dados_jogo)
        
    df = pd.DataFrame(lista_banco)
        
    conn = sqlite3.connect('brasileirao_predict.db')
    df.to_sql('partidas', conn, if_exists='append', index=False)
    
    conn.close()
if __name__ == "__main__":
    ingest_temporada(2024)