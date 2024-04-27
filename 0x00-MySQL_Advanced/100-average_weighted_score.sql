-- a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and store the average weighted score for a student.

DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
	DECLARE avg_weighted_score DECIMAL(10, 2);
	
	SELECT IF(
		SUM(score * weight) > 0,
		SUM(score * weight) / SUM(weight),
		0) INTO avg_weighted_score
	FROM corrections
	JOIN projects ON corrections.project_id = projects.id
	WHERE corrections.user_id = user_id;
	
	UPDATE users
	SET average_weighted_score = avg_weighted_score
	WHERE id = user_id;
END //
DELIMITER ;
