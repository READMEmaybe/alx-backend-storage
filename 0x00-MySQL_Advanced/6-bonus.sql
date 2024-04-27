-- a SQL script that creates a stored procedure AddBonus that adds a new correction for a student.
-- The procedure takes three parameters:
--  - user_id, an integer that represents the id of the student
--  - project_name, a string that represents the name of the project
--  - score, an integer that represents the score of the correction
DELIMITER //

CREATE PROCEDURE AddBonus(IN user_id INT, IN project_name VARCHAR(255), IN score INT)
BEGIN
	DECLARE project_id INT;
	
	-- Check if project_name exists in projects table
	SELECT id INTO project_id FROM projects WHERE name = project_name;
	
	-- If project_name doesn't exist, create it
	IF project_id IS NULL THEN
		INSERT INTO projects (name) VALUES (project_name);
		SET project_id = LAST_INSERT_ID();
	END IF;
	
	-- Insert the new correction
	INSERT INTO corrections (user_id, project_id, score) VALUES (user_id, project_id, score);
END //

DELIMITER ;
