USE ara_ara;

DROP PROCEDURE IF EXISTS delete_post;

DELIMITER //
CREATE PROCEDURE delete_post(IN idpost INT)
BEGIN
    UPDATE post SET ativo = 0 WHERE id_post = idpost;
END//
DELIMITER ;