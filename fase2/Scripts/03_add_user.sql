USE ara_ara;

DROP PROCEDURE IF EXISTS add_user;

DELIMITER //
CREATE PROCEDURE add_user(IN new_name VARCHAR(50), IN new_email VARCHAR(50),IN new_city INT)
BEGIN
    INSERT INTO usuario (Nome, Email, id_cidade) VALUES (new_name, new_email, new_city);
END//
DELIMITER ;