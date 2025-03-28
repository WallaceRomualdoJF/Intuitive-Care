# Teste de Web Scraping - ANS

Este projeto realiza **web scraping** para baixar documentos da página da **Agência Nacional de Saúde Suplementar (ANS)**, verificando o conteúdo dos PDFs e compactando-os em um arquivo ZIP.

## Objetivo

- Acessar a página da ANS
- Encontrar os links dos anexos **I** e **II** (PDFs)
- Baixar os documentos
- Verificar o conteúdo dos PDFs
- Compactar os arquivos válidos em um ZIP

---

## Tecnologias Utilizadas

- **Python 3.7+**
- **Requests** → Para acessar a página web
- **BeautifulSoup4** → Para extrair os links dos PDFs
- **PyMuPDF (fitz)** → Para ler e verificar o conteúdo dos PDFs
- **zipfile** → Para compactação dos arquivos

---

## Instalação

Antes de executar o script, instale as dependências necessárias. Execute o comando abaixo no terminal (PowerShell, CMD ou Bash):

```sh
pip install requests beautifulsoup4 pymupdf
```

Se estiver usando Python 3.11, pode ser necessário instalar os pacotes.

---

## Execução

Após a instalação, execute o script:

```sh
python web_scraping_ans.py
```

---

## 📂 Estrutura do Projeto

```
📂 1 - TESTE DE WEB SCRAPING
 ├── 📄 web_scraping_ans.py  # Código principal
 ├── 📁 downloads/            # Diretório onde os PDFs serão salvos
 ├── 📦 anexos_compactados.zip  # Arquivo ZIP gerado com os PDFs válidos
 ├── 📄 README.md            # Este arquivo
```

---

## Explicação do Código

1. **Obter os links dos PDFs** na página da ANS.
2. **Baixar os arquivos** correspondentes aos anexos I e II.
3. **Verificar o conteúdo dos PDFs** para garantir que não estão vazios.
4. **Compactar os arquivos válidos** em um único ZIP.

---

## Resultado Esperado

Após a execução bem-sucedida:
- Os PDFs serão baixados em `downloads/`.
- O arquivo compactado `anexos_compactados.zip` será gerado com os PDFs válidos.
- Se algum PDF estiver vazio, ele não será incluído no ZIP.

---

