import os
import requests
import fitz  # PyMuPDF para leitura de PDFs
from bs4 import BeautifulSoup
import zipfile

URL = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

DOWNLOAD_DIR = "downloads"
ZIP_FILE = "anexos_compactados.zip"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def obter_links_pdfs(url):
    
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Erro ao acessar a página: {response.status_code}")
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Encontrar todos os links que apontam para PDFs
    links = [a["href"] for a in soup.find_all("a", href=True) if a["href"].lower().endswith(".pdf")]
    
    # Filtrar os anexos desejados
    anexos = [link for link in links if "anexo-i" in link.lower() or "anexo-ii" in link.lower()]
    
    if not anexos:
        raise Exception("Nenhum anexo encontrado!")
    
    return anexos

def baixar_arquivos(links):
    arquivos_baixados = []
    
    for link in links:
        nome_arquivo = os.path.join(DOWNLOAD_DIR, link.split("/")[-1])
        
        response = requests.get(link, stream=True)
        if response.status_code == 200:
            with open(nome_arquivo, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            arquivos_baixados.append(nome_arquivo)
            print(f"Download concluído: {nome_arquivo}")
        else:
            print(f"Erro ao baixar: {link}")
    
    return arquivos_baixados

def verificar_conteudo_pdf(arquivo):
    try:
        doc = fitz.open(arquivo)  # Abre o PDF
        texto = ""
        
        for pagina in doc:
            texto += pagina.get_text("text")  # Extrai o texto
        
        doc.close()
        
        # Se o PDF estiver vazio, retorna falso
        if not texto.strip():
            print(f"O arquivo {arquivo} parece estar vazio ou ilegível.")
            return False
        
        # Exibir um trecho do conteúdo como exemplo
        print(f"Trecho do PDF {os.path.basename(arquivo)}:\n")
        print(texto[:500])  # Exibir os primeiros 500 caracteres para conferir
        
        return True
    
    except Exception as e:
        print(f"Erro ao processar {arquivo}: {e}")
        return False

def compactar_arquivos(arquivos, nome_zip):

    with zipfile.ZipFile(nome_zip, "w") as zipf:
        for arquivo in arquivos:
            zipf.write(arquivo, os.path.basename(arquivo))
    
    print(f"Arquivos compactados em: {nome_zip}")

# Execução do processo
try:
    print("Buscando links dos PDFs...")
    links_pdfs = obter_links_pdfs(URL)
    
    print("Baixando arquivos...")
    arquivos_baixados = baixar_arquivos(links_pdfs)
    
    print("Verificando conteúdo dos PDFs...")
    arquivos_validos = [arquivo for arquivo in arquivos_baixados if verificar_conteudo_pdf(arquivo)]
    
    if arquivos_validos:
        print("Compactando arquivos válidos...")
        compactar_arquivos(arquivos_validos, ZIP_FILE)
    else:
        print("Nenhum arquivo válido encontrado para compactação.")
    
    print("Processo concluído com sucesso!")

except Exception as e:
    print(f" Erro: {e}")