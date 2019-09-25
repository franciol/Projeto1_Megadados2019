USE ara_ara;

DROP PROCEDURE IF EXISTS tag_bird;

DELIMITER //
CREATE PROCEDURE tag_bird(IN id_bird INT, IN idpost INT)
BEGIN
    INSERT INTO menciona_passaro (id_post, id_passaro) VALUES (idpost, id_bird);
END//
DELIMITER ;