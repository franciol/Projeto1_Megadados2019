USE ara_ara;

DROP PROCEDURE IF EXISTS delete_user;

DELIMITER //
CREATE PROCEDURE delete_user(IN id_user INT)
BEGIN
    UPDATE usuario SET ativo = 0 WHERE id_usuario = id_user;
END//
DELIMITER ;