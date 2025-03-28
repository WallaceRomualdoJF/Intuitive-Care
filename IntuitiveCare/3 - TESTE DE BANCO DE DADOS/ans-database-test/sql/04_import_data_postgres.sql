-- Importação de dados para PostgreSQL
\c ans_operadoras;

-- Importar dados das operadoras
COPY operadoras FROM '/caminho/completo/operadoras_ativas.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';

-- Importar dados contábeis (execute para cada arquivo, ajustando o caminho)
COPY demonstracoes_contabeis (registro_ans, competencia, conta_contabil, descricao, valor)
FROM '/caminho/completo/demonstracao_contabil_202301.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';