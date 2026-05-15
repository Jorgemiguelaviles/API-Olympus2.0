DROP DATABASE olympius;
CREATE DATABASE olympius;
USE olympius;


CREATE TABLE usuarios (
    funcional BIGINT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    nome VARCHAR(100) NOT NULL
);


CREATE TABLE atividade (
    codigo_atividade BIGINT AUTO_INCREMENT PRIMARY KEY,
    nome_atividade VARCHAR(50) NOT NULL UNIQUE,
    path_atividade VARCHAR(255) NOT NULL
);


CREATE TABLE atividade_realizada (
    id_atividade_realizada BIGINT AUTO_INCREMENT PRIMARY KEY,
    
    data_hora TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    descricao VARCHAR(255),

    funcional BIGINT NOT NULL,
    codigo_atividade BIGINT NOT NULL,

    CONSTRAINT fk_usuario
        FOREIGN KEY (funcional)
        REFERENCES usuarios(funcional),

    CONSTRAINT fk_atividade
        FOREIGN KEY (codigo_atividade)
        REFERENCES atividade(codigo_atividade)
);