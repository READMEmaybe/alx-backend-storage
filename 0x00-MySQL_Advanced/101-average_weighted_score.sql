-- a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers
-- that computes and store the average weighted score for all students.
-- Procedure ComputeAverageWeightedScoreForUsers is not taking any input.

DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
	DECLARE avg_weighted_score DECIMAL(10, 2);
	
	SELECT SUM(corrections.score * projects.weight) / SUM(projects.weight) INTO avg_weighted_score
	FROM corrections
	JOIN projects ON corrections.project_id = projects.id
	WHERE corrections.user_id = users.id;
	
	UPDATE users
	SET average_score = avg_weighted_score;
END //
DELIMITER ;
