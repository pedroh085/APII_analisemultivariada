import json
import pandas as pd
import os

# Caminho para o arquivo de entrada
input_file = 'sinistros-2015-2024.geojson'

# 1. Carregar o arquivo GeoJSON
with open(input_file, 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

# 2. Extrair os atributos (properties) de cada ponto
records = []
for feature in geojson_data.get('features', []):
    # O GeoJSON armazena as informações da tabela na chave 'properties'
    prop = feature.get('properties', {})
    records.append(prop)

# 3. Converter para um DataFrame do Pandas
df = pd.DataFrame(records)

# 4. Salvar o arquivo CSV completo
main_csv = 'sinistros_2015_2024_completo.csv'
df.to_csv(main_csv, index=False, encoding='utf-8')

# 5. Criar a pasta para os arquivos individuais
output_folder = 'acidentes por ano csv'
os.makedirs(output_folder, exist_ok=True)

# 6. Agrupar os dados por ano e salvar um CSV para cada
if 'ANO' in df.columns:
    # Remove valores nulos caso existam e pega os anos únicos
    years = sorted(df['ANO'].dropna().unique())
    
    for year in years:
        # Filtra o DataFrame apenas com os registros daquele ano
        df_year = df[df['ANO'] == year]
        
        # Define o caminho do arquivo dentro da pasta criada
        file_path = os.path.join(output_folder, f'sinistros_{int(year)}.csv')
        
        # Salva o resultado
        df_year.to_csv(file_path, index=False, encoding='utf-8')