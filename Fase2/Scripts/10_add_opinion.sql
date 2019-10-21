USE ara_ara;

DROP PROCEDURE IF EXISTS add_opinion;

DELIMITER //
CREATE PROCEDURE add_opinion(IN id_user INT, IN idpost INT, IN opinion INT) /* 0 = dislike, 1 = like, 2 = cancela */
label:BEGIN
	DELETE FROM joinha WHERE id_usuario = id_user AND id_post = idpost;
	IF opinion = 2 
    THEN
		LEAVE label;
	ELSE   
		INSERT INTO joinha (id_usuario, id_post, joinha) VALUES (id_user, idpost, opinion); 
    
    
END IF ;
END//
DELIMITER ;