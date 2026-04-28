from connection import run_query

# Question 7-8
def get_broadband_data(local_authority, ward):
    # Query for question 7
    query1 = """
    SELECT ba.area_name, bm.avg_download_speed_mbps, ROUND(bm.superfast_availability * 100, 2) || "%" as superfast_pct
    FROM broadband_metric bm
    JOIN broadband_area ba ON bm.area_code = ba.area_code
    WHERE ba.area_name = ?
    """

    # Set parameters for the query
    params1 = (ward,)

    # Execute the query with parameters
    broadband_stats = run_query(query1, params=params1)

    # Query for question 8
    query2 = """
    SELECT ba.area_name, ROUND(bm.avg_download_speed_mbps, 2) AS average_speed_mbps, 
    ROUND(bm.superfast_availability * 100, 1) AS Superfast_Pct, ROUND(bm.gigabit_availability * 100, 1) AS Gigabit_Pct
	FROM broadband_metric bm
	JOIN broadband_area ba ON bm.area_code = ba.area_code
	JOIN local_authority l ON ba.local_authority_code = l.local_authority_code
	WHERE l.local_authority_name = ?
	ORDER BY bm.avg_download_speed_mbps DESC
	LIMIT 5;
    """

    # Set parameters for the query
    params2 = (local_authority,)

    # Execute the query for question 8
    broadband_fastest = run_query(query2, params=params2)

    print(broadband_stats)

    return broadband_stats, broadband_fastest

get_broadband_data("Cherwell", "Bicester North")
