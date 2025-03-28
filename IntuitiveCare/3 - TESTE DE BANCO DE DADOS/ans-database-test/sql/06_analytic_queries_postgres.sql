-- Queries analíticas para PostgreSQL
\c ans_operadoras;

-- 1 - METODO POR MES: 10 operadoras com maiores despesas no último trimestre
WITH ultimo_trimestre AS (
    SELECT 
        DATE_TRUNC('month', MAX(competencia) - INTERVAL '2 months') AS data_inicio,
        (DATE_TRUNC('month', MAX(competencia)) + INTERVAL '1 month' - INTERVAL '1 day')::date AS data_fim
    FROM demonstracoes_contabeis
)
SELECT 
    o.razao_social,
    o.nome_fantasia,
    o.registro_ans,
    TO_CHAR(SUM(d.valor), 'FM999G999G990D00') AS total_despesas,
    'Último Trimestre' AS periodo
FROM 
    demonstracoes_contabeis d
JOIN 
    operadoras o ON d.registro_ans = o.registro_ans
JOIN 
    ultimo_trimestre t ON d.competencia BETWEEN t.data_inicio AND t.data_fim
WHERE 
    d.descricao LIKE '%EVENTOS/%SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'
GROUP BY 
    o.razao_social, o.nome_fantasia, o.registro_ans
ORDER BY 
    SUM(d.valor) DESC
LIMIT 10;

-- 2 - METODO POR ANO: 10 operadoras com maiores despesas no último ano
WITH ultimo_ano AS (
    SELECT 
        (DATE_TRUNC('year', MAX(competencia)) - INTERVAL '1 year')::date AS data_inicio,
        (DATE_TRUNC('year', MAX(competencia)) + INTERVAL '1 year' - INTERVAL '1 day')::date AS data_fim
    FROM demonstracoes_contabeis
)
SELECT 
    o.razao_social,
    o.nome_fantasia,
    o.registro_ans,
    TO_CHAR(SUM(d.valor), 'FM999G999G990D00') AS total_despesas,
    'Último Ano' AS periodo
FROM 
    demonstracoes_contabeis d
JOIN 
    operadoras o ON d.registro_ans = o.registro_ans
JOIN 
    ultimo_ano a ON d.competencia BETWEEN a.data_inicio AND a.data_fim
WHERE 
    d.descricao LIKE '%EVENTOS/%SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'
GROUP BY 
    o.razao_social, o.nome_fantasia, o.registro_ans
ORDER BY 
    SUM(d.valor) DESC
LIMIT 10;