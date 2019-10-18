USE ara_ara;

DROP PROCEDURE IF EXISTS edit_bio;

DELIMITER //
CREATE PROCEDURE edit_bio(IN nome varchar(50), IN image VARCHAR(512), IN txt VARCHAR(200), IN id_user INT)
BEGIN
	DELETE FROM bio WHERE id_usuario = id_user;
    INSERT INTO bio (id_usuario, Nome_completo, Foto_perfil, Descricao) VALUES (id_user, nome, image, txt);
END//
DELIMITER ;