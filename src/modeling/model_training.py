import pandas as pd
import sqlite3

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

conn = sqlite3.connect('tb_modelagem.db')

df_model = pd.read_sql('SELECT * FROM model_input', conn)

conn.close()

df_ml = df_model.copy()
print(f"Total de linhas no dataset: {len(df_ml)}")

df_ml = pd.get_dummies(df_ml, columns=['mandante', 'visitante'], dtype=int)

y = df_ml['resultado']
x = df_ml.drop(columns=['resultado', 'data'])

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=20)

forest_model = RandomForestClassifier(n_estimators=100, random_state=20)

forest_model.fit(x_train, y_train)

previsoes = forest_model.predict(x_test)

precisao = accuracy_score(y_test, previsoes)

print(previsoes)
print(precisao)

# --- EXPORTAÇÃO PARA O EXCEL (AMOSTRA DE 20 JOGOS) ---

# 1. Resgatamos as linhas originais usando o índice do x_test
df_excel = df_model.loc[x_test.index].copy()

# 2. Filtramos apenas as colunas que importam
df_excel = df_excel[['mandante', 'visitante', 'resultado']]
df_excel = df_excel.rename(columns={'resultado': 'resultado_real'})

# 3. Adicionamos a coluna com os chutes da nossa IA
df_excel['resultado_previsto'] = previsoes

# 4. Reorganizamos a ordem das colunas
df_excel = df_excel[['mandante', 'visitante', 'resultado_previsto', 'resultado_real']]

# 5. O FILTRO DE OURO: Cortamos a tabela para ter exatamente 20 linhas
df_excel = df_excel.head(20)

# 6. Exportamos para Excel
try:
    df_excel.to_excel('resultados_ia.xlsx', index=False)
    print("Arquivo 'resultados_ia.xlsx' gerado com sucesso (Amostra de 20 jogos)!")
except ImportError:
    # Se você não tiver a biblioteca 'openpyxl', ele salva em CSV
    df_excel.to_csv('resultados_ia.csv', sep=';', index=False, encoding='utf-8-sig')
    print("Arquivo 'resultados_ia.csv' gerado com sucesso (Amostra de 20 jogos)!")