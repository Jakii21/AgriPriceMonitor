import pandas as pnds


def cleanData(finalDf):

    df = finalDf.copy()

    print("\n--- TRANSFORM ---")
    print("Records before cleaning:", len(df))

    # Standardize column names---------------------------------
    df.columns = [column.strip().lower()
        for column in df.columns]

    # Make sure price is numeric ---------------------------------
    df["price"] = pnds.to_numeric(df["price"],errors="coerce")

    # Make sure price_date is a date ---------------------------------
    df["price_date"] = pnds.to_datetime(df["price_date"],errors="coerce").dt.date

    # ***Report how many records removed each cleaning stage
    before_price_filter = len(df)

    # Remove records with invalid prices ---------------------------------
    df = df[df["price"].notna() & (df["price"] > 0)]

    # **************************************************
    invalid_prices_removed = ( before_price_filter - len(df))
    print( "Invalid prices removed:", invalid_prices_removed )

    # ***Report how many records removed each cleaning stage
    before_duplicates = len(df)

    # Remove duplicate records ---------------------------------
    df = df.drop_duplicates(
        subset=["price_date", "market", "item", "specification"])

    #**************************************************
    duplicates_removed = (before_duplicates - len(df))
    print( "Duplicates removed:",duplicates_removed)

    # Clean text fields ---------------------------------
    text_columns = ["category", "city", "market", "item", "specification"]

    for column in text_columns:
        df[column] = df[column].astype(str).str.strip()

    # ----------------Clean specification------------------------------

    df["specification"] = ( df["specification"]
        .replace("", pnds.NA)
        .replace("N/A", pnds.NA)
        .str.strip() )

    #------------------------------------------------------------------
    print("Records after cleaning:", len(df))

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    print(df.isnull().sum())

    return df


def validateData(df):

        print("\n--- VALIDATION ---")

        required_columns = ["price_date", "category", "city", "market",
                            "item", "specification","price"]

        # Check required columns
        missing_columns = [column for column in required_columns if column not in df.columns]

        if missing_columns:
            print("Missing columns:",missing_columns)
            return False

        # Check missing values
        missing_values = df[required_columns].isnull().sum()

        print("\nMissing values:")
        print(missing_values)

        # Check invalid prices
        invalid_prices = df[
            df["price"].isnull() | (df["price"] <= 0)]

        print("\nInvalid price records: ", len(invalid_prices) )

#------------------- validate the allowed cities, markets, and categories -------------------

        allowed_cities = {"Paranaque", "Las Pinas", "Muntinlupa"}

        allowed_markets = {
            "NEW LAS PINAS CITY PUBLIC MARKET",
            "PAMILIHANG LUNGSOD NG MUNTINLUPA",
            "LA HUERTA MARKET"  }

        allowed_categories = { "Rice", "Fruits", "Highland Vegetables",
                               "Lowland Vegetables", "Meat & Poultry" }

        invalid_cities = df[
            ~df["city"].isin(allowed_cities) ]

        invalid_markets = df[
            ~df["market"].isin(allowed_markets) ]

        invalid_categories = df[  ~df["category"].isin(allowed_categories) ]

        # ---------------------------------------------------------------

        print("Invalid cities:", len(invalid_cities))
        print("Invalid markets:", len(invalid_markets))
        print("Invalid categories:", len(invalid_categories))

        # Final validation result
        if (len(invalid_prices) > 0
            or len(invalid_cities) > 0
            or len(invalid_markets) > 0
            or len(invalid_categories) > 0):
            print("\nValidation failed.")

            return False

        print("\nValidation passed.")

    #-----------------------Clean specification----------------------------------------
        missing_specifications = df[
            df["specification"].isna() ]

        print("Missing specifications:",len(missing_specifications))
        print("\n")

        return True

    #---------------------------------------------------------------
