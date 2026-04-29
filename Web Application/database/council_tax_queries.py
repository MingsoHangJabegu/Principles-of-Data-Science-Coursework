from .connection import run_query

# Question 9-10
def get_council_tax_data(ward_1, ward_2):
    # Query for question 9
    query1 = """
        WITH Town1 AS (
            SELECT cta.area_name, ctr.tax_amount
            FROM council_tax_rate ctr
            JOIN council_tax_area cta ON ctr.area_id = cta.area_id
            AND cta.area_name = ?
            AND ctr.tax_band = 'A'
        ),
        Town2 AS (
            SELECT cta.area_name, ctr.tax_amount
            FROM council_tax_rate ctr
            JOIN council_tax_area cta ON ctr.area_id = cta.area_id
            AND cta.area_name = ?
            AND ctr.tax_band = 'A'
        )
        SELECT 
            Town1.area_name AS Area_1,
            Town1.tax_amount AS Charge_1,
            Town2.area_name AS Area_2,
            Town2.tax_amount AS Charge_2,
            ABS(Town1.tax_amount - Town2.tax_amount) AS Tax_Difference
        FROM Town1, Town2;
    """

    # Set parameters for the query
    params1 = (ward_1, ward_2)

    # Execute the query with parameters
    tax_diff = run_query(query1, params=params1)

    # Query for question 10
    query2 = """
        SELECT cta.area_name AS Town, ctr.tax_amount AS Lowest_Tax
        FROM council_tax_rate ctr
        JOIN council_tax_area cta ON ctr.area_id = cta.area_id
        WHERE ctr.tax_band = 'B'
        ORDER BY ctr.tax_amount ASC           
        LIMIT 1;                           
    """

    # Execute the query for question 10
    lowest_tax = run_query(query2)
    return(tax_diff, lowest_tax)