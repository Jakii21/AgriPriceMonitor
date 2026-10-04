USE agriproject_db;

DROP VIEW IF EXISTS vw_price_analysis;

CREATE VIEW vw_price_analysis AS
SELECT
    pr.price_id,
    pr.price_date,
    c.city_name,
    m.market_name,
    cat.category_name,
    i.item_name,
    pr.specification,
    pr.price_average,
    pr.currency,
    s.source_name
FROM price_records pr
JOIN markets m
    ON pr.market_id = m.market_id
JOIN cities c
    ON m.city_id = c.city_id
JOIN items i
    ON pr.item_id = i.item_id
JOIN categories cat
    ON i.category_id = cat.category_id
JOIN sources s
    ON pr.source_id = s.source_id;