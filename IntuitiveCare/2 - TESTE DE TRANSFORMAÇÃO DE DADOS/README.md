
## Script Python: `processar_pdf_tabelas.py`

Script para extrair, processar e exportar tabelas de PDFs da ANS (Agência Nacional de Saúde Suplementar).

### Funcionalidades:
- Extração de tabelas de PDFs complexos
- Processamento e estruturação dos dados
- Substituição de abreviaturas por termos completos
- Exportação para CSV compactado em ZIP

### Como usar
1. Coloque o PDF na mesma pasta do script
2. Execute o comando:
```bash
python processar_pdf_tabelas.py
```

### Estrutura do Código

```python
import pandas as pd
import pdfplumber
import zipfile
import os
```

### Fluxo de Processamento
1. **Extração de tabelas**:
   ```python
   def extrair_tabelas_pdf(caminho_pdf):
       # Implementação da extração
   ```

2. **Processamento dos dados**:
   ```python
   def processar_tabelas(tabelas):
       # Organização em DataFrame
   ```

3. **Substituição de abreviaturas**:
   ```python
   def substituir_abreviaturas(df):
       # Conversão OD → Seguro Odontológico, etc.
   ```

4. **Exportação dos resultados**:
   ```python
   def salvar_zip(df, nome_saida):
       # Gera CSV e compacta em ZIP
   ```

### Saída
- Arquivo `Teste_Wallace.zip` contendo:
  - Dados estruturados em CSV
  - Todas as colunas originais processadas

### Requisitos
- Python 3.6+
- Bibliotecas:
  ```bash
  pip install pandas pdfplumber
  ```

### Solução de Problemas

Se encontrar erros:
1. Verifique se o PDF está no local correto
2. Confira as permissões de arquivo
3. Valide a estrutura do PDF de entrada