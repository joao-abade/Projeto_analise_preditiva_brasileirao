import sqlite3

def create_database():
    # Conecta (ou cria) o banco de dados
    conn = sqlite3.connect('brasileirao_predict.db')
    cursor = conn.cursor()

    # Criando a tabela de partidas (Camada Bronze - Raw Data)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS partidas_raw (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            temporada INTEGER NOT NULL,
            rodada INTEGER NOT NULL,
            mandante TEXT NOT NULL,
            visitante TEXT NOT NULL,
            gols_mandante INTEGER,
            gols_visitante INTEGER,
            xg_mandante REAL,
            xg_visitante REAL,
            posse_mandante REAL,
            posse_visitante REAL,
            clima_temp REAL,
            clima_condicao TEXT,
            precip_mm,
            descanso_mandante INTEGER,
            descanso_visitante INTEGER,
            resultado_final TEXT -- 'H' (Home), 'A' (Away), 'D' (Draw)
        )
    ''')

    # Tabela para guardar as predições do modelo e comparar depois
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predicoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            partida_id INTEGER,
            prob_vitoria_mandante REAL,
            prob_empate REAL,
            prob_vitoria_visitante REAL,
            modelo_versao TEXT,
            FOREIGN KEY (partida_id) REFERENCES partidas_raw (id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Banco de dados e tabelas criados com sucesso!")

if __name__ == "__main__":
    create_database()