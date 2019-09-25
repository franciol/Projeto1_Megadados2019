USE ara_ara;

DROP PROCEDURE IF EXISTS add_post;

DELIMITER //
CREATE PROCEDURE add_post(IN title varchar(50), IN image VARCHAR(512), IN txt VARCHAR(200), IN id_user INT)
BEGIN
    INSERT INTO post (Titulo, Imagem, Texto, id_usuario) VALUES (title, image, txt, id_user);
END//
DELIMITER ;