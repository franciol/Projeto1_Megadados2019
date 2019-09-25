USE ara_ara;

DROP PROCEDURE IF EXISTS tag_user;

DELIMITER //
CREATE PROCEDURE tag_user(IN id_user INT, IN idpost INT)
BEGIN
    INSERT INTO menciona_usuario (id_post, id_usuario) VALUES (idpost, id_user);
END//
DELIMITER ;