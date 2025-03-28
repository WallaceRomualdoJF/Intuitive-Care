
**Sistema de Busca de Operadoras Ativas**  

---

## **Visão Geral**  
Projeto full-stack para busca e visualização de dados de operadoras de saúde ativas no Brasil, com:  
- **Backend**: API em Python (FastAPI) para processamento e busca dos dados.  
- **Frontend**: Interface web em Vue.js 3 para interação com o usuário.  
- **Dados**: Base original em `.ods` (convertida para `.csv` automaticamente).  

---

## **Tecnologias**  
| **Backend**       | **Frontend**       | **Ferramentas**        |  
|-------------------|--------------------|------------------------|  
| Python 3.8+       | Vue.js 3           | Vite (build tool)      |  
| FastAPI           | PrimeVue (UI)      | Pandas (processamento) |  
| Uvicorn (server)  | Axios (HTTP)       | Levenshtein (busca)    |  

---

## **📂 Estrutura de Arquivos**  
```markdown
projeto-operadoras/  

├── backend/  
│   ├── main.py               # API principal  
│   ├── requirements.txt      # Dependências Python  
│   └── data/  
│       ├── dicionario_de_dados_das_operadoras_ativas.ods    # Fonte original  
│       └── dicionario_de_dados_das_operadoras_ativas.csv    # Gerado automaticamente  
│  
├── frontend/  
│   ├── public/               # Assets estáticos  
│   ├── src/  
│   │   ├── components/  
│   │   │   └── SearchOperadoras.vue    # Componente de busca  
│   │   ├── App.vue           # Componente raiz  
│   │   └── main.js           # Inicialização Vue  
│   ├── package.json          # Dependências Node  
│   └── vite.config.js        # Configuração do Vite  
│  
└── README.md                 # Este arquivo  
```

---

## **Como Executar**  

### **1. Backend (FastAPI)**  
```bash
cd backend  
pip install -r requirements.txt  # Instala dependências  
python main.py                  # Inicia servidor em http://localhost:8000  
```

### **2. Frontend (Vue.js)**  
```bash
cd frontend  
npm install                     # Instala dependências  
npm run dev                    # Inicia app em http://localhost:5173  
```

> **Informação**: Execute os dois servidores em terminais separados no VSCODE ou IntelliJ IDEA

---

## **Funcionalidades**  
1. **Busca textual** por nome, CNPJ, região, etc.  
2. **Ordenação** por relevância (algoritmo de Levenshtein).  
3. **Filtros avançados** por campo específico.  
4. **Visualização em tabela** com paginação.  

---

## **Rotas da API (Backend)**  
| Rota                          | Método | Descrição                          |  
|-------------------------------|--------|------------------------------------|  
| `/api/operadoras/search`      | GET    | Busca operadoras por termo         |  
| `/api/operadoras/fields`      | GET    | Lista campos disponíveis           |  

**Exemplo de busca**:  
```bash
curl "http://localhost:8000/api/operadoras/search?query=saude&max_results=5"  
```

---

## **Dicas para Desenvolvimento**  
- **Backend**:  
  - Edite `main.py` para adicionar novos filtros ou lógica de busca.  
  - Use `pd.read_csv()` para carregar os dados.  

- **Frontend**:  
  - Modifique `SearchOperadoras.vue` para ajustar a interface.  
  - Adicione novos componentes em `/src/components/`.  

---

## **Build para Produção**  
```bash
cd frontend  
npm run build  # Gera arquivos otimizados em /dist/  
```  
Sirva a pasta `dist/` com Nginx, Apache ou Netlify.  

---