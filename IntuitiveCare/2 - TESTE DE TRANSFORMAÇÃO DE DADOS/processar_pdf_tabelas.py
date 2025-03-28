import pandas as pd
import pdfplumber
import zipfile
import os
   
def extrair_tabelas_pdf(caminho_pdf):
    """
    Extrai tabelas do PDF do Anexo I da RN 465/2021 e Retorna uma lista de tabelas encontradas no documento
    """
    tabelas = []
    
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            # Extrai tabelas de cada página
            tabelas_pagina = pagina.extract_tables()
            
            # Para cada tabela na página
            for tabela in tabelas_pagina:
                # Remove linhas vazias e cabeçalhos duplicados
                tabela_limpa = []
                for linha in tabela:
                    # Filtra linhas que não são totalmente vazias
                    if any(celula and str(celula).strip() for celula in linha):
                        tabela_limpa.append(linha)
                
                # Adiciona à lista de tabelas se não estiver vazia
                if tabela_limpa:
                    tabelas.append(tabela_limpa)
    
    return tabelas

def processar_tabelas(tabelas):
    """
    Processa as tabelas extraídas para criar um DataFrame estruturado e Retorna um pandas DataFrame com os dados organizados
    """
    dados = []
    colunas = [
        'PROCEDIMENTO', 'RN_alteracao', 'VIGENCIA', 'OD', 'AMB', 'HCO', 'HSO', 
        'REF', 'PAC', 'DUT', 'SUBGRUPO', 'GRUPO', 'CAPITULO'
    ]
    
    for tabela in tabelas:
        # Verifica se a primeira linha contém cabeçalhos
        if 'PROCEDIMENTO' in str(tabela[0]):
            cabecalho = tabela[0]
            linhas = tabela[1:]
        else:
            # Se não tiver cabeçalho, assume que é continuação da tabela anterior
            linhas = tabela
        
        for linha in linhas:
            # Garante que a linha tem o número correto de colunas
            if len(linha) == len(colunas):
                dados.append(linha)
            elif len(linha) > len(colunas):
                # Se tiver mais colunas, pega apenas as que precisamos
                dados.append(linha[:len(colunas)])
            else:
                # Se tiver menos colunas, completa com None
                linha_completa = linha + [None] * (len(colunas) - len(linha))
                dados.append(linha_completa)
    
    df = pd.DataFrame(dados, columns=colunas)

    df = df[df['PROCEDIMENTO'] != 'PROCEDIMENTO']

    df = df.dropna(how='all')
    
    return df

def substituir_abreviaturas(df):
    """
    Substitui as abreviações OD e AMB pelas descrições completas conforme legenda e Retorna o DataFrame com as substituições realizadas
    """
    # Substituições conforme legenda no rodapé
    substituicoes = {
        'OD': 'Seguro Odontológico',
        'AMB': 'Seguro Ambulatorial',
        'HCO': 'Seguro Hospitalar Com Obstetrícia',
        'HSO': 'Seguro Hospitalar Sem Obstetrícia',
        'REF': 'Plano Referência',
        'PAC': 'Procedimento de Alta Complexidade',
        'DUT': 'Diretriz de Utilização'
    }
    
    # Substitui os valores nas colunas OD e AMB
    df['OD'] = df['OD'].apply(lambda x: substituicoes['OD'] if x == 'OD' else x)
    df['AMB'] = df['AMB'].apply(lambda x: substituicoes['AMB'] if x == 'AMB' else x)
    
    return df

def salvar_zip(df, nome_saida):
    """
    Salva o DataFrame em CSV e compacta em arquivo ZIP
    Gera um arquivo com o nome no formato "Teste_{nome}.zip" solicitado
    """
    nome_csv = f"Teste_{nome_saida}.csv"
    nome_zip = f"Teste_{nome_saida}.zip"
    
    # Salva CSV com codificação para caracteres especiais
    df.to_csv(nome_csv, index=False, encoding='utf-8-sig')
    
    # Cria arquivo ZIP
    with zipfile.ZipFile(nome_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(nome_csv)
    
    os.remove(nome_csv)
    
    print(f"Arquivo {nome_zip} criado com sucesso!")

def principal(caminho_pdf, seu_nome):
    """
    Função principal que orquestra todo o processo:
    1. Extrai tabelas do PDF
    2. Processa os dados
    3. Substitui abreviaturas
    4. Salva em arquivo ZIP
    """
    try:
        print("Iniciando extração de dados do PDF...")
        
        # Extrai tabelas do PDF
        tabelas = extrair_tabelas_pdf(caminho_pdf)
        print(f"Extraídas {len(tabelas)} tabelas do PDF")
        
        # Processa as tabelas em um DataFrame
        df = processar_tabelas(tabelas)
        print(f"Processadas {len(df)} linhas de dados")
        
        # Substitui abreviaturas
        df = substituir_abreviaturas(df)
        print("Abreviações substituídas com sucesso")
        
        salvar_zip(df, seu_nome)
        
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")

if __name__ == "__main__":

    caminho_do_pdf = "Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
    seu_nome = "Wallace"
    
    principal(caminho_do_pdf, seu_nome)