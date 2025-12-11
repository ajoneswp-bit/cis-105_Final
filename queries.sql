SELECT 
    ranked.position_rank,
    ranked.player_name,
    ranked.position,
    ranked.total_points,
    ROUND((COALESCE(ranked.week_11, 0) + COALESCE(ranked.week_12, 0) + COALESCE(ranked.week_13, 0)) / 3.0, 2) as last_3_weeks_avg,
    ranked.week_11,
    ranked.week_12,
    ranked.week_13
FROM (
    SELECT 
        ROW_NUMBER() OVER (PARTITION BY position ORDER BY total_points DESC) as position_rank,
        player_name, 
        position, 
        total_points,
        week_11,
        week_12,
        week_13
    FROM player_stats
) ranked
ORDER BY last_3_weeks_avg DESC; 