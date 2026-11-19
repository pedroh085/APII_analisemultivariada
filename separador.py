import json
import os

def separar_geojson_por_ano(arquivo_entrada):
    print(f"Lendo o arquivo {arquivo_entrada}...")
    
    # Carrega o arquivo GeoJSON original
    with open(arquivo_entrada, 'r', encoding='utf-8') as f:
        dados = json.load(f)
        
    # Obtém o sistema de referência de coordenadas (CRS), se existir, para repassar aos novos arquivos
    crs_padrao = dados.get("crs", {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::4674"}})
    
    # Dicionário para armazenar a estrutura FeatureCollection de cada ano
    dados_por_ano = {}
    
    # Itera sobre todas as feições (acidentes)
    for feature in dados.get('features', []):
        ano = feature.get('properties', {}).get('ANO')
        
        # Se for um ano válido entre 2015 e 2024
        if ano and 2015 <= ano <= 2024:
            # Inicializa a estrutura para o ano caso ainda não exista
            if ano not in dados_por_ano:
                dados_por_ano[ano] = {
                    "type": "FeatureCollection",
                    "name": f"Sinistros-{ano}",
                    "crs": crs_padrao,
                    "features": []
                }
            
            # Adiciona o acidente à lista do ano correspondente
            dados_por_ano[ano]['features'].append(feature)
            
    # Salva os novos arquivos GeoJSON
    print("\nGerando os arquivos separados...")
    for ano, conteudo_geojson in sorted(dados_por_ano.items()):
        nome_arquivo = f"sinistros-{ano}.geojson"
        
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(conteudo_geojson, f, ensure_ascii=False, separators=(',', ':'))
            
        quantidade = len(conteudo_geojson['features'])
        print(f"✅ {nome_arquivo} criado com sucesso ({quantidade} sinistros).")

# Executa a função passando o nome do seu arquivo
if __name__ == "__main__":
    nome_do_arquivo = "sinistros-2015-2024.geojson"
    
    # Verifica se o arquivo existe antes de rodar
    if os.path.exists(nome_do_arquivo):
        separar_geojson_por_ano(nome_do_arquivo)
    else:
        print(f"Erro: O arquivo '{nome_do_arquivo}' não foi encontrado no diretório atual.")