import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "http://www.bantaypresyo.da.gov.ph"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

PROXIES = {
    "http": None,
    "https": None
}

REGION = "130000000"

TARGET_MARKETS = {
    "NEW LAS PINAS CITY PUBLIC MARKET": "Las Pinas",
    "PAMILIHANG LUNGSOD NG MUNTINLUPA": "Muntinlupa",
    "LA HUERTA MARKET": "Paranaque"
}

COMMODITIES = {
    "1": {
        "name": "Rice",
        "header_endpoint": "/tbl_price_get_comm_header_rice.php",
        "price_endpoint": "/tbl_price_get_comm_price_rice.php"
    },
    "5": {
        "name": "Fruits",
        "header_endpoint": "/tbl_price_get_comm_header_meat.php",
        "price_endpoint": "/tbl_price_get_comm_price_meat.php"
    },
    "6": {
        "name": "Highland Vegetables",
        "header_endpoint": "/tbl_price_get_comm_header_meat.php",
        "price_endpoint": "/tbl_price_get_comm_price_meat.php"
    },
    "7": {
        "name": "Lowland Vegetables",
        "header_endpoint": "/tbl_price_get_comm_header_meat.php",
        "price_endpoint": "/tbl_price_get_comm_price_meat.php"
    },
    "8": {
        "name": "Meat & Poultry",
        "header_endpoint": "/tbl_price_get_comm_header_meat.php",
        "price_endpoint": "/tbl_price_get_comm_price_meat.php"
    }
}

#-----------------------------------------------------------------------------------------------

def get_date(commodity_id):

    url = f"{BASE_URL}/tbl_rice.php"

    paylaod = {
        "action": "get_latest_date",
        "region": REGION,
        "commodity": commodity_id
    }

    response = requests.post(url, data=paylaod, headers=HEADERS, timeout=10, proxies=PROXIES)

    price_date = pd.to_datetime(response.text.strip()).date()

    return price_date

#-----------------------------------------------------------------------------------------------

def get_market_headers(commodity_id):

    endpoint = COMMODITIES[commodity_id]["header_endpoint"]

    url = f"{BASE_URL}{endpoint}"

    payload = {
        "commodity": commodity_id,
        "region": REGION
    }

    response = requests.post(url, data=payload, headers=HEADERS, timeout=10, proxies=PROXIES)

    soup = BeautifulSoup(response.text,"html.parser")

    headers = []

    for cell in soup.find_all(["td", "th"]):
        text = cell.get_text(strip=True)
        headers.append(text)

    return headers

#-----------------------------------------------------------------------------------------------
def get_price_rows(commodity_id):

    endpoint = COMMODITIES[commodity_id]["price_endpoint"]

    url = f"{BASE_URL}{endpoint}"

    paylaod = {
        "commodity": commodity_id,
        "region": REGION }

    response = requests.post(url, data=paylaod, headers=HEADERS, timeout=10, proxies=PROXIES)

    soup = BeautifulSoup(response.text,"html.parser")

    rows = soup.find_all("tr")

    return rows

#-----------------------------------------------------------------------------------------------
                  #Table rows      #Header names         #Date        #Category Name
def build_records(rowss, headers, price_date, categoryName):

    records = []

    for row in rowss:
        cells = row.find_all("td")

        if len(cells) < 3:
            continue

        commodity = cells[0].get_text(strip=True)
        specification = cells[1].get_text(strip=True)

        for i in range(2, len(cells)):

            market = headers[i]
            price = cells[i].get_text(strip=True)

            if market in TARGET_MARKETS and price != "N/A":

                records.append({
                    "price_date": price_date,
                    "category": categoryName,
                    "city": TARGET_MARKETS[market],
                    "market": market,
                    "item": commodity,
                    "specification": specification,
                    "price": float(price)
                })
    return records

#-----------------------------------------------------------------------------------------------

def scrape_category(commodity_id):

    categoryName = COMMODITIES[commodity_id]["name"]

    priceDate = get_date(commodity_id)

    headers = get_market_headers(commodity_id)

    price_rows = get_price_rows(commodity_id)

    records = build_records(price_rows, headers, priceDate, categoryName)

    df = pd.DataFrame(records)

    return df

#-------------------------------------------------------------------------------------------

def scrape_all():


    allData = []

    for cmmdty in COMMODITIES:
        df = scrape_category(cmmdty)            # This is where the commodity_id came from
        allData.append(df)

    finalDf = pd.concat(allData,ignore_index=True)

    return finalDf
#-------------------------------------------------------------------------------------------





























