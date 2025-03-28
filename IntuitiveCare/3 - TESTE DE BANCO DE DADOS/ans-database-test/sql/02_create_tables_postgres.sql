-- Criação das tabelas para PostgreSQL 10.0 oui superior
CREATE DATABASE ans_operadoras;

\c ans_operadoras;

-- Tabela de Operadoras
CREATE TABLE IF NOT EXISTS operadoras (
    registro_ans VARCHAR(20) PRIMARY KEY,
    cnpj VARCHAR(20),
    razao_social VARCHAR(255),
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(100),
    logradouro VARCHAR(255),
    numero VARCHAR(50),
    complemento VARCHAR(100),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    uf VARCHAR(2),
    cep VARCHAR(10),
    ddd VARCHAR(5),
    telefone VARCHAR(20),
    fax VARCHAR(20),
    endereco_eletronico VARCHAR(255),
    representante VARCHAR(255),
    cargo_representante VARCHAR(100),
    data_registro_ans DATE
);

-- Tabela de Demonstrações Contábeis
CREATE TABLE IF NOT EXISTS demonstracoes_contabeis (
    id SERIAL PRIMARY KEY,
    registro_ans VARCHAR(20) REFERENCES operadoras(registro_ans),
    competencia DATE,
    conta_contabil VARCHAR(100),
    descricao VARCHAR(255),
    valor DECIMAL(15, 2)
);

-- Criar índices para melhorar performance
CREATE INDEX idx_dc_competencia ON demonstracoes_contabeis(competencia);
CREATE INDEX idx_dc_descricao ON demonstracoes_contabeis(descricao);