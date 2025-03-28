# Solução para o Teste de Banco de Dados - ANS

Este repositório contém a solução para o teste de banco de dados envolvendo dados abertos da Agência Nacional de Saúde Suplementar (ANS).

## Descrição do Projeto

O projeto consiste em:
1. Estruturar um banco de dados para armazenar informações das operadoras de saúde ativas
2. Importar dados contábeis das demonstrações financeiras das operadoras
3. Desenvolver queries analíticas para identificar as operadoras com maiores despesas em assistência médico-hospitalar

## 📂 Estrutura de Arquivos
ans-database-test/
├── sql/
│ ├── 01_create_tables_mysql.sql # Script de criação de tabelas para MySQL
│ ├── 02_create_tables_postgres.sql # Script de criação de tabelas para PostgreSQL
│ ├── 03_import_data_mysql.sql # Script de importação para MySQL
│ ├── 04_import_data_postgres.sql # Script de importação para PostgreSQL
│ ├── 05_analytic_queries_mysql.sql # Queries analíticas para MySQL
│ └── 06_analytic_queries_postgres.sql # Queries analíticas para PostgreSQL
├── data/ # Pasta para armazenar os arquivos CSV baixados
├── README.md # Este arquivo


## Pré-requisitos

- MySQL 8.0+ ou PostgreSQL 10.0+
- Arquivos CSV baixados dos portais de dados abertos da ANS:
  - [Operadoras Ativas](https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/)
  - [Demonstrações Contábeis](https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/) (últimos 2 anos)

## Queries Analíticas Implementadas
1. Top 10 operadoras com maiores despesas em "EVENTOS/SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR" no último trimestre

2. Top 10 operadoras com maiores despesas na mesma categoria no último ano

## Configuração
Antes de executar os scripts de importação, edite os arquivos 03_import_data_mysql.sql ou 04_import_data_postgres.sql para apontar para os caminhos corretos dos arquivos CSV na sua máquina.