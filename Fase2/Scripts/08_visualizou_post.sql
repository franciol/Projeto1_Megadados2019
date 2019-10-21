USE ara_ara;

DROP PROCEDURE IF EXISTS visu_post;

DELIMITER //
CREATE PROCEDURE visu_post(IN id_user INT, IN idpost INT, IN os INT,IN browser INT,IN IP INT,IN horario DATETIME)
BEGIN
    INSERT INTO viu_post (id_usuario, id_post, id_OS, id_browser, IP, horario) VALUES (id_user, idpost, os, browser,IP,horario);
END//
DELIMITER ;