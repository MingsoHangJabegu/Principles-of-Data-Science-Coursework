from .connection import run_query

# Question 4-6
def get_house_prices_data(local_authority, ward,start_year, end_year, quarter):
    # Query for question 4
    query1 = """
    SELECT w.ward_name, AVG(hp.median_price) AS average_price
    FROM house_price hp 
    JOIN ward w ON hp.ward_code = w.ward_code 
    WHERE w.ward_name = ? AND (hp.period LIKE ? OR hp.period LIKE ?)
    """

    # Set parameters for the query
    params1 = (ward, f"%{start_year}", f"%{end_year}")

    # Execute the query with parameters
    average_prices = run_query(query1, params=params1)


    # Query for question 5
    query2 ="""
    WITH Year1 AS (
        SELECT ward_code, AVG(median_price) as avg_price_1
        FROM house_price WHERE period LIKE ? GROUP BY ward_code
    ),
    Year2 AS (
        SELECT ward_code, AVG(median_price) as avg_price_2
        FROM house_price WHERE period LIKE ? GROUP BY ward_code
    )
    SELECT w.ward_name, ((y2.avg_price_2 - y1.avg_price_1) / y1.avg_price_1) * 100.0 || "%" AS pct_change
    FROM ward w
    JOIN Year1 y1 ON w.ward_code = y1.ward_code
    JOIN Year2 y2 ON w.ward_code = y2.ward_code
    WHERE w.ward_name = ?;
    """

    # Set parameters for the query
    params2 = (f"%{start_year}", f"%{end_year}", ward)

    # Execute the query with parameters
    price_changes = run_query(query2, params=params2)

    # Query for question 6
    query3 = """
    SELECT w.ward_name, hp.median_price
    FROM house_price hp
    JOIN ward w ON hp.ward_code = w.ward_code
    JOIN local_authority l ON w.local_authority_code = l.local_authority_code
    WHERE l.local_authority_name = ? AND hp.period = ?
    ORDER BY hp.median_price ASC
    LIMIT 1;
    """

    # Set parameters for the query
    params3 = (local_authority, quarter)

    # Execute the query with parameters
    lowest_price = run_query(query3, params=params3)
    return average_prices, price_changes, lowest_price