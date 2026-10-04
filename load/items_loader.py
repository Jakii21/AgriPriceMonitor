from load.db_connection import get_connection

# MARKET MAPPING ----------------------------------------------------
market_mapping = {
    "NEW LAS PINAS CITY PUBLIC MARKET": "New Las Pinas City Public Market",
    "PAMILIHANG LUNGSOD NG MUNTINLUPA": "Pamilihang Lungsod ng Muntinlupa",
    "LA HUERTA MARKET": "La Huerta Market"
}

# GET MARKET ID ----------------------------------------------------
def get_market_id(sqlConnect, market_name):

    sql_crsr = sqlConnect.cursor()

    query = """
        SELECT market_id
        FROM markets
        WHERE market_name = %s
    """

    sql_crsr.execute(query, (market_name,))

    result = sql_crsr.fetchone()

    sql_crsr.close()

    if result:
        return result[0]

    return None


# GET ITEM ID ----------------------------------------------------
def get_item_id(sqlConnect, itemName):

    sql_crsr = sqlConnect.cursor()

    query = """
        SELECT item_id
        FROM items
        WHERE item_name = %s
    """

    sql_crsr.execute(query, (itemName,))

    result = sql_crsr.fetchone()

    sql_crsr.close()

    if result:
        return result[0]

    return None


# INSERT PRICE RECORD ----------------------------------------------------
def insert_price_record(sqlConnect,price_date,market_id,item_id,
                        source_id,specification,price):

    sql_crsr = sqlConnect.cursor()

    query = """
        INSERT INTO price_records
        (
            price_date,
            market_id,
            item_id,
            source_id,
            specification,
            price_average
        )
        VALUES (%s, %s, %s, %s, %s, %s)

        ON DUPLICATE KEY UPDATE
            specification = VALUES(specification),
            price_average = VALUES(price_average)
    """

    sql_crsr.execute(query,(price_date,market_id,item_id,source_id,specification,price))

    sqlConnect.commit()

    if sql_crsr.rowcount == 1:
        status = "Inserted"
    elif sql_crsr.rowcount == 2:
        status = "Updated"
    elif sql_crsr.rowcount == 0:
        status = "No change"

    sql_crsr.close()

    return status


# LOAD PRICES ----------------------------------------------------

def load_prices(finalDf):

    sqlConnect = get_connection()

    source_id = 1

    inserted_count = 0
    updated_count = 0
    no_change_count = 0
    skipped_count = 0
    error_count = 0

    for index, row in finalDf.iterrows():

        # DA market name
        da_market = row["market"]

        # Convert DA market name
        # to MySQL market name
        mysql_market = market_mapping[da_market]

        # Get market ID
        market_id = get_market_id(sqlConnect,mysql_market)

        # Get item name
        item_name = row["item"]

        # Get item ID
        item_id = get_item_id(sqlConnect,item_name)

        # Check market
        if market_id is None:

            print("Market not found:",mysql_market)

            skipped_count += 1

            continue

        # Check item
        if item_id is None:

            print("Item not found:",item_name)

            skipped_count += 1

            continue

        # Insert price record
        status = insert_price_record(
            sqlConnect,
            row["price_date"],
            market_id,
            item_id,
            source_id,
            row["specification"],
            row["price"] )

        if status == "Inserted":

            inserted_count += 1

        elif status == "Updated":

            updated_count += 1

        elif status == "No change":

            no_change_count += 1

        print(status,":", item_name, "|", mysql_market, "|", row["price"])

    print("\n---*   LOAD SUMMARY   *---")
    print("Inserted:", inserted_count)
    print("Updated:", updated_count)
    print("No change:", no_change_count)
    print("Skipped:", skipped_count)
    print("Errors:", error_count)

    sqlConnect.close()