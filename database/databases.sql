DROP DATABASE olympius;
CREATE DATABASE olympius;
USE olympius;

-- Tabela de usuários
-- CREATE TABLE usuarios (
--     funcional BIGINT AUTO_INCREMENT PRIMARY KEY,
--     usuario VARCHAR(50) NOT NULL UNIQUE,
--     senha_hash VARCHAR(255) NOT NULL,
--     nome VARCHAR(100) NOT NULL
--     usuario_root BOOLEAN NOT NULL
--     usuario_ativado BOOLEAN NOT NULL
-- );

-- Catálogo de atividades possíveis
CREATE TABLE atividade (
    codigo_atividade CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    nome_atividade VARCHAR(50) NOT NULL UNIQUE
);

-- Histórico de atividades executadas
CREATE TABLE atividade_realizada (
    id_atividade_realizada BIGINT AUTO_INCREMENT PRIMARY KEY,
    data_hora TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    descricao VARCHAR(255),

    funcional BIGINT NOT NULL,
    codigo_atividade CHAR(36) NOT NULL,

    -- FOREIGN KEY (funcional) 
    --     REFERENCES usuarios(funcional),

    FOREIGN KEY (codigo_atividade) 
        REFERENCES atividade(codigo_atividade)
);



-- massas de testes

INSERT INTO atividade (nome_atividade)
VALUES
('RUN'),
('SWIM'),
('CYCL'),
('WALK'),
('YOGA');

SELECT * FROM atividade;






INSERT INTO atividade_realizada (
    funcional,
    codigo_atividade,
    descricao
)
VALUES

(
    1001,
    (SELECT codigo_atividade FROM atividade WHERE nome_atividade = 'RUN'),
    'Corrida de 5km'
),

(
    1001,
    (SELECT codigo_atividade FROM atividade WHERE nome_atividade = 'SWIM'),
    'Natação de 30 minutos'
),

(
    1002,
    (SELECT codigo_atividade FROM atividade WHERE nome_atividade = 'CYCL'),
    'Ciclismo de 12km'
),

(
    1002,
    (SELECT codigo_atividade FROM atividade WHERE nome_atividade = 'WALK'),
    'Caminhada de recuperação'
),

(
    1003,
    (SELECT codigo_atividade FROM atividade WHERE nome_atividade = 'YOGA'),
    'Sessão de mobilidade'
);

select * from atividade_realizada;
