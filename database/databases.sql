CREATE DATABASE olympius;
USE olympius;

-- Tabela de usuários
 CREATE TABLE usuarios (
     funcional BIGINT AUTO_INCREMENT PRIMARY KEY,
     usuario VARCHAR(50) NOT NULL UNIQUE,
     senha_hash VARCHAR(255) NOT NULL,
     nome VARCHAR(100) NOT NULL,
     usuario_root BOOLEAN NOT NULL,
     usuario_ativado BOOLEAN NOT NULL
);

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

    FOREIGN KEY (funcional) 
         REFERENCES usuarios(funcional),

    FOREIGN KEY (codigo_atividade) 
        REFERENCES atividade(codigo_atividade)
);


