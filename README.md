# **Intuitive Care**

## **Visão Geral**  
Intuitive Care consiste em 4 testes técnicos, avaliando habilidades em:  
✅ **Web Scraping**  
✅ **Transformação de Dados**  
✅ **Banco de Dados (SQL)**  
✅ **Desenvolvimento de API (Vue.js + Backend)**  

---

## **Teste 1 - Web Scraping**  
### **Tarefas:**  
1. Acessar o site da ANS e baixar os **Anexos I a IV** ([link](https://www.gov.br/ans/pt-br/assuntos/consumidor/o-que-o-seu-plano-de-saude-deve-cobrir-1/o-que-e-o-rol-de-procedimentos-e-evento-em-saude)).  
2. Agrupar os arquivos em um **.zip** ou **.rar**.  

### **Tecnologias Sugeridas:**  
- Python: `requests`, `BeautifulSoup`, `zipfile`  
- Java: `Jsoup`, `HttpClient`, `ZipOutputStream`  

---

## **Teste 2 - Transformação de Dados**  
### **Tarefas:**  
1. Extrair dados da **tabela do Anexo I (PDF)**.  
2. Salvar em **CSV** com estrutura adequada.  
3. Substituir abreviações (**OD → Odontológico, AMB → Ambulatorial**).  
4. Compactar em `Teste_{Seu_Nome}.zip`.  

### **Tecnologias Sugeridas:**  
- Python: `PyPDF2`, `pandas`, `csv`  
- Java: `Apache PDFBox`, `OpenCSV`  

---

## **Teste 3 - Banco de Dados**  
### **Tarefas:**  
1. Baixar arquivos contábeis dos últimos **2 anos** ([dados.ans.gov.br](https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/)).  
2. Criar tabelas SQL e carregar os dados.  
3. Consultas analíticas:  
   - **Top 10 operadoras** com mais despesas em **"Eventos/Sinistros de Assistência Médico-Hospitalar"** no:  
     - **Último trimestre**  
     - **Último ano**  

### **Tecnologias Sugeridas:**  
- SQL: `CREATE TABLE`, `COPY` (PostgreSQL), `LOAD DATA` (MySQL)  
- Consultas com `GROUP BY`, `SUM`, `ORDER BY`, `LIMIT`  

---

## **Teste 4 - API + Frontend**  
### **Tarefas:**  
1. Criar um **servidor** (Python) com uma rota de **busca textual** em um CSV de operadoras.  
2. Desenvolver uma **interface Vue.js** para consumir a API.   

### **Tecnologias Sugeridas:**  
- Backend: **FastAPI** (Python), **Flask**  
- Frontend: **Vue 3** (Composition API)  
- Ferramentas: **Postman**, **GitHub/GitLab**