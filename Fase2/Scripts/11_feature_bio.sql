USE ara_ara;
DROP TABLE IF EXISTS bio;

CREATE TABLE bio (
    id_usuario INT NOT NULL,
	Nome_completo VARCHAR(50) NOT NULL,
    Foto_perfil VARCHAR(512),
    Descricao Varchar(200),
    PRIMARY KEY (id_usuario),
    FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario)
);
