import requests
from bs4 import BeautifulSoup

header_url = "http://www.bantaypresyo.da.gov.ph/tbl_price_get_comm_header_rice.php"
price_url = "http://www.bantaypresyo.da.gov.ph/tbl_price_get_comm_price_rice.php"

data = {
    "commodity": "1",
    "region": "130000000"
}

# Get headers
response = requests.post(header_url, data=data)
soup = BeautifulSoup(response.text, "html.parser")

headers = [
    cell.get_text(strip=True)
    for cell in soup.find_all(["td", "th"])
]

# Target markets
target_markets = [
    "NEW LAS PINAS CITY PUBLIC MARKET",
    "PAMILIHANG LUNGSOD NG MUNTINLUPA",
    "LA HUERTA MARKET"
]

# Get prices
response = requests.post(price_url, data=data)
soup = BeautifulSoup(response.text, "html.parser")

rows = soup.find_all("tr")

# Test first 3 rows
for row in rows[1:4]:

    cells = row.find_all("td")

    commodity = cells[0].get_text(strip=True)
    specification = cells[1].get_text(strip=True)

    print("\nCommodity:", commodity)
    print("Specification:", specification)

    for i in range(2, len(cells)):

        market = headers[i]
        price = cells[i].get_text(strip=True)

        if market in target_markets and price != "N/A":
            print(market, "=", price)