DROP DATABASE IF EXISTS ara_ara;
CREATE DATABASE ara_ara;
USE ara_ara;

CREATE TABLE cidade (
    id_cidade INT NOT NULL AUTO_INCREMENT,
    Nome VARCHAR(50) NOT NULL,
    PRIMARY KEY (id_cidade)
);

CREATE TABLE passaro (
    id_passaro INT NOT NULL AUTO_INCREMENT,
    Nome VARCHAR(50) NOT NULL,
    PRIMARY KEY (id_passaro)
);

CREATE TABLE OS (
    id_OS INT NOT NULL AUTO_INCREMENT,
    Nome VARCHAR(50) NOT NULL,
    PRIMARY KEY (id_OS)
);
CREATE TABLE browser (
    id_browser INT NOT NULL AUTO_INCREMENT,
    Nome VARCHAR(50) NOT NULL,
    PRIMARY KEY (id_browser)
);

CREATE TABLE usuario (
    id_usuario INT NOT NULL AUTO_INCREMENT,
    Nome VARCHAR(50) NOT NULL,
    Email VARCHAR(50) NOT NULL,
    id_cidade INT NOT NULL,
    ativo TINYINT NOT NULL DEFAULT 1,
    PRIMARY KEY (id_usuario),
    FOREIGN KEY (id_cidade) REFERENCES cidade (id_cidade)
);

CREATE TABLE post (
    id_post INT NOT NULL AUTO_INCREMENT,
    Titulo VARCHAR(50) NOT NULL,
    Imagem VARCHAR(512),
    Texto Varchar(200),
    id_usuario INT NOT NULL,
    ativo TINYINT NOT NULL DEFAULT 1,
    PRIMARY KEY (id_post),
    FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario)
);

CREATE TABLE preferencia (
    id_usuario INT NOT NULL,
    id_passaro INT NOT NULL,
    PRIMARY KEY (id_usuario, id_passaro),
    FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario),
    FOREIGN KEY (id_passaro) REFERENCES passaro (id_passaro)
);

CREATE TABLE menciona_usuario (
    id_post INT NOT NULL,
    id_usuario INT NOT NULL,
    ativo INT NOT NULL DEFAULT 1, 
    PRIMARY KEY (id_usuario, id_post),
    FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario),
    FOREIGN KEY (id_post) REFERENCES post (id_post)
);

CREATE TABLE menciona_passaro (
    id_post INT NOT NULL,
    id_passaro INT NOT NULL,
    ativo INT NOT NULL DEFAULT 1,
    PRIMARY KEY (id_passaro, id_post),
    FOREIGN KEY (id_passaro) REFERENCES passaro (id_passaro),
    FOREIGN KEY (id_post) REFERENCES post (id_post)
);

CREATE TABLE viu_post (
    id_usuario INT NOT NULL,
    id_post INT NOT NULL,
    id_OS INT NOT NULL,
    id_browser INT NOT NULL,
    IP VARCHAR(100) ,
    horario DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_post, id_usuario),
    FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario),
    FOREIGN KEY (id_post) REFERENCES post (id_post),
    FOREIGN KEY (id_OS) REFERENCES OS (id_OS),
    FOREIGN KEY (id_browser) REFERENCES browser (id_browser)
);