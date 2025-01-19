import os
import json
import shutil
from datetime import datetime
from collections import Counter

def organizar_arquivos_recursivo(diretorio_origem, diretorio_destino):
    if not os.path.exists(diretorio_destino):
        os.makedirs(diretorio_destino)

    for root, _, arquivos in os.walk(diretorio_origem):
        for arquivo in arquivos:
            if arquivo.endswith('.json'):
                caminho_completo = os.path.join(root, arquivo)

                with open(caminho_completo, 'r', encoding='utf-8') as f:
                    metadados = json.load(f)

                if 'photoTakenTime' in metadados and 'timestamp' in metadados['photoTakenTime']:
                    timestamp = int(metadados['photoTakenTime']['timestamp'])
                    ano = datetime.fromtimestamp(timestamp).year
                else:
                    ano = 'Sem_Data'

                pasta_ano = os.path.join(diretorio_destino, str(ano))
                if not os.path.exists(pasta_ano):
                    os.makedirs(pasta_ano)

                # Move o arquivo JSON
                shutil.move(caminho_completo, os.path.join(pasta_ano, arquivo))

                # Procura e move o arquivo de mídia correspondente de forma recursiva
                if 'title' in metadados:
                    nome_midia = metadados['title']
                    midia_encontrada = False

                    for root_midia, _, arquivos_midia in os.walk(diretorio_origem):
                        if nome_midia in arquivos_midia:
                            caminho_midia = os.path.join(root_midia, nome_midia)
                            shutil.move(caminho_midia, os.path.join(pasta_ano, nome_midia))
                            print(f"Arquivo de mídia movido: {nome_midia}")
                            midia_encontrada = True
                            break

                    if not midia_encontrada:
                        print(f"Aviso: Mídia não encontrada: {nome_midia}")
                else:
                    print(f"Aviso: Campo 'title' não encontrado no JSON: {arquivo}")

    print("Organização concluída!")

def organizar_sem_json(diretorio_origem, diretorio_destino):
    extensoes_para_pastas = {
        '.jpg': 'Imagens',
        '.jpeg': 'Imagens',
        '.png': 'Imagens',
        '.gif': 'Imagens',
        '.mp4': 'Videos',
        '.mov': 'Videos',
        '.avi': 'Videos',
        '.doc': 'Documentos',
        '.docx': 'Documentos',
        '.pdf': 'Documentos',
        '.txt': 'Documentos',
        '.xlsx': 'Documentos',
        '.pptx': 'Documentos',
        '.zip': 'Comprimidos',
        '.rar': 'Comprimidos',
        '.7z': 'Comprimidos',
        '.tar': 'Comprimidos',
        '.gz': 'Comprimidos',
        '.html': 'Web',
        '.css': 'Web',
        '.js': 'Web',
        '.cryptmf': 'Outros',
        '.ttf': 'Outros',
        '.svg': 'Outros',
        '.eot': 'Outros',
        '.woff': 'Outros',
        '.otf': 'Outros',
        '.scss': 'Web'
    }

    for root, _, arquivos in os.walk(diretorio_origem):
        for arquivo in arquivos:
            if not arquivo.endswith('.json'):
                extensao = os.path.splitext(arquivo)[1].lower()
                if extensao in extensoes_para_pastas:
                    pasta_destino = os.path.join(diretorio_destino, extensoes_para_pastas[extensao])
                    if not os.path.exists(pasta_destino):
                        os.makedirs(pasta_destino)

                    caminho_arquivo = os.path.join(root, arquivo)
                    shutil.move(caminho_arquivo, os.path.join(pasta_destino, arquivo))
                    print(f"Arquivo movido: {arquivo} para {pasta_destino}")

def validar_arquivos_restantes(diretorio_origem):
    extensoes = []

    for root, _, arquivos in os.walk(diretorio_origem):
        for arquivo in arquivos:
            extensao = os.path.splitext(arquivo)[1].lower()
            extensoes.append(extensao)

    contagem_extensoes = Counter(extensoes)
    
    if not contagem_extensoes:
        print("Nenhum arquivo encontrado no diretório de origem.")
    else:
        print("Arquivos restantes no diretório de origem:")
        for extensao, quantidade in contagem_extensoes.items():
            print(f"{extensao}: {quantidade} arquivo(s)")
    
    return contagem_extensoes

# Uso do script
diretorio_origem = '/run/media/wilson/DADOS/Google/descompactados/Takeout'
diretorio_destino = '/run/media/wilson/DADOS/Google/organizado'

# Chamando as funções
organizar_arquivos_recursivo(diretorio_origem, diretorio_destino)
organizar_sem_json(diretorio_origem, diretorio_destino)
validar_arquivos_restantes(diretorio_origem)
