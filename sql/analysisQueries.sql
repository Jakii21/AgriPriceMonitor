USE agriproject_db;

--- Average / minimum / maximum by item and market

SELECT
    item_name,
    city_name,
    market_name,
    MIN(price_average) AS minimum_price,
    MAX(price_average) AS maximum_price,
    ROUND(AVG(price_average), 2) AS average_price
FROM vw_price_analysis
GROUP BY
    item_name,
    city_name,
    market_name
ORDER BY
    item_name,
    city_name;


--- Average price by market

SELECT
    city_name,
    market_name,
    ROUND(AVG(price_average), 2) AS average_price
FROM vw_price_analysis
GROUP BY
    city_name,
    market_name
ORDER BY
    average_price DESC;


--- Category analysis

SELECT
    category_name,
    ROUND(AVG(price_average), 2) AS average_price,
    MIN(price_average) AS minimum_price,
    MAX(price_average) AS maximum_price,
    COUNT(*) AS total_records
FROM vw_price_analysis
GROUP BY
    category_name
ORDER BY
    category_name;


---Latest available date

SELECT
    MAX(price_date) AS latest_price_date
FROM vw_price_analysis;

--- Records by date

SELECT
    price_date,
    COUNT(*) AS total_records
FROM vw_price_analysis
GROUP BY
    price_date
ORDER BY
    price_date DESC;


--- Market comparison

SELECT
    item_name,
    city_name,
    market_name,
    ROUND(AVG(price_average), 2) AS average_price
FROM vw_price_analysis
GROUP BY
    item_name,
    city_name,
    market_name
ORDER BY
    item_name,
    average_price;


--- Market price difference

SELECT
    item_name,
    MIN(average_price) AS lowest_market_price,
    MAX(average_price) AS highest_market_price,
    ROUND(
        MAX(average_price) - MIN(average_price),
        2
    ) AS price_difference
FROM
(
    SELECT
        item_name,
        market_name,
        AVG(price_average) AS average_price
    FROM vw_price_analysis
    GROUP BY
        item_name,
        market_name
) AS market_prices
GROUP BY
    item_name
ORDER BY
    price_difference DESC;


