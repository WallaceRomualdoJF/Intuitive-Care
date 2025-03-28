-- Queries analíticas para MySQL
USE ans_operadoras;

-- 1 - 10 operadoras com maiores despesas no último trimestre
WITH ultimo_trimestre AS (
    SELECT 
        DATE_FORMAT(MAX(competencia), '%Y-%m-01') AS data_inicio,
        LAST_DAY(MAX(competencia)) AS data_fim
    FROM demonstracoes_contabeis
)
SELECT 
    o.razao_social,
    o.nome_fantasia,
    o.registro_ans,
    FORMAT(SUM(d.valor), 2, 'de_DE') AS total_despesas,
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

-- 2 - 10 operadoras com maiores despesas no último ano
WITH ultimo_ano AS (
    SELECT 
        DATE_FORMAT(DATE_SUB(MAX(competencia), INTERVAL 1 YEAR), '%Y-%m-01') AS data_inicio,
        LAST_DAY(MAX(competencia)) AS data_fim
    FROM demonstracoes_contabeis
)
SELECT 
    o.razao_social,
    o.nome_fantasia,
    o.registro_ans,
    FORMAT(SUM(d.valor), 2, 'de_DE') AS total_despesas,
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