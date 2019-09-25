USE ara_ara;

DROP PROCEDURE IF EXISTS add_preference;

DELIMITER //
CREATE PROCEDURE add_preference(IN id_user INT, IN id_bird INT)
BEGIN
    INSERT INTO preferencia (id_usuario, id_passaro) VALUES (id_user, id_bird);
END//
DELIMITER ;