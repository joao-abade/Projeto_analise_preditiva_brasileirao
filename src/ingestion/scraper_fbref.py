import pandas as pd
import sqlite3
import time
import requests
import cloudscraper

def ingest_fbref_data(ano):
    url = f"https://fbref.com/pt/comps/24/{ano}/cronograma/{ano}-Serie-A-Resultados-e-Calendarios"
    
    print(f"Iniciando captura de dados de {ano}") #Markpoint para verificar se está rodando
    
    try:
        scraper = cloudscraper.create_scraper(browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        })
        resposta = scraper.get(url)
        if resposta.status_code != 200:
            print(f"O site bloqueou. Código: {resposta.status_code}")
            return
        
        tabs = pd.read_html(resposta.text)
        df = tabs[0]
        
        df = df[['Data', 'Rodada', 'Mandante', 'Placar', 'Visitante', 'xG', 'xG.1']]
        
        df.columns = ['data', 'rodada', 'mandante', 'placar', 'visitante', 'xg_mandante', 'xg_visitante']
        
        df = df.dropna(subset=['data'])
        df = df[df['data'] != 'Data']
        
        df[['gols_mandante', 'gols_visitante']] = df['placar'].str.split('-', expand = True)
        
        def define_resultado(linha):
            if pd.isna(linha['gols_mandante']): return None
            gm = int(linha['gols_mandante'])
            gv = int(linha['gols_visitante'])
            if gm > gv: return 'H'
            if gv > gm: return 'A'
            return 'D'
        
        df['resultado_final'] = df.apply(define_resultado, axis=1)
        df['temporada'] = ano
        
        conn = sqlite3.connect('../../brasileirao_predict.db')
        
        df.to_sql('partidas_raw', conn, if_exists='append', index=False)
        
        conn.close()
        print(f'Temporada {ano} salva com sucesso no banco')
        
    except Exception as e:
        print(f"Erro ao processar: {e}")

if __name__ == "__main__":
    anos = [2023, 2024]
    
    for ano in anos:
        ingest_fbref_data(ano)
        
        time.sleep(5)