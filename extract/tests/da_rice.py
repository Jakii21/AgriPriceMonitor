import requests
import pandas as pnds
from bs4 import BeautifulSoup

URL = "http://www.bantaypresyo.da.gov.ph"

payload = {
    "commodity": "1",
    "region": "130000000"}

# Requesting to get Date
date_request = requests.post(f"{URL}/tbl_rice.php",data={"action": "get_latest_date",**payload})

price_date = pnds.to_datetime(date_request.text.strip()).date()

# Get market headers
header_request = requests.post(f"{URL}/tbl_price_get_comm_header_rice.php",data=payload)

header_soup = BeautifulSoup(header_request.text,"html.parser")

headers = []

for cell in header_soup.find_all(["th"]):
    text = cell.get_text(strip=True)
    headers.append(text)

# Get prices
price_response = requests.post(f"{URL}/tbl_price_get_comm_price_rice.php",data=payload)

price_soup = BeautifulSoup(price_response.text,"html.parser")

rows = price_soup.find_all("tr")

target_markets = {
    "NEW LAS PINAS CITY PUBLIC MARKET": "Las Pinas",
    "PAMILIHANG LUNGSOD NG MUNTINLUPA": "Muntinlupa",
    "LA HUERTA MARKET": "Paranaque"
}

records = []

for row in rows:
    cellsRow = row.find_all("td")

    if len(cellsRow) < 3:
        continue

    commodity = cellsRow[0].get_text(strip=True)
    specification = cellsRow[1].get_text(strip=True)

    for i in range(2, len(cellsRow)):

        market = headers[i]
        price = cellsRow[i].get_text(strip=True)

        if market in target_markets and price != "N/A":

            records.append({
                "price_date": price_date,
                "city": target_markets[market],
                "market": market,
                "item": commodity,
                "specification": specification,
                "price": float(price)
            })

df = pnds.DataFrame(records)

print(df)
print("\nTotal records:", len(df))

print("\n--- DATA PREVIEW ---")
print(df)

print("\n--- DATA INFO ---")
print(df.info())

print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

print("\nTotal records:", len(df))

print("\n--- CITIES ---")
print(df["city"].unique())

print("\n--- MARKETS ---")
print(df["market"].unique())