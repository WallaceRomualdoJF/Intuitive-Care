-- Importação de dados para MySQL
USE ans_operadoras;

-- Importar dados das operadoras (ajuste o caminho do arquivo)
LOAD DATA INFILE '/caminho/completo/operadoras_ativas.csv'
INTO TABLE operadoras
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(registro_ans, cnpj, razao_social, nome_fantasia, modalidade, 
logradouro, numero, complemento, bairro, cidade, uf, cep, 
ddd, telefone, fax, endereco_eletronico, representante, 
cargo_representante, @data_registro_ans)
SET data_registro_ans = STR_TO_DATE(@data_registro_ans, '%d/%m/%Y');

-- Importar dados contábeis (execute para cada arquivo, ajustando o caminho)
LOAD DATA INFILE '/caminho/completo/demonstracao_contabil_202301.csv'
INTO TABLE demonstracoes_contabeis
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(registro_ans, @competencia, conta_contabil, descricao, @valor)
SET 
    competencia = STR_TO_DATE(@competencia, '%d/%m/%Y'),
    valor = REPLACE(REPLACE(@valor, '.', ''), ',', '.');