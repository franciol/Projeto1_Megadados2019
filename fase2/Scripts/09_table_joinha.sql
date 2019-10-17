USE ara_ara;
DROP TABLE IF EXISTS joinha;

CREATE TABLE joinha (
    id_post INT NOT NULL,
    id_usuario INT NOT NULL,
    joinha TINYINT NOT NULL, /*0 = dislike, 1 = like*/
    PRIMARY KEY (id_usuario, id_post),
    FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario),
    FOREIGN KEY (id_post) REFERENCES post (id_post)
);
