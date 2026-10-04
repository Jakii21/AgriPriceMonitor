import requests
from bs4 import BeautifulSoup

# 1. Get market headers

header_url = "http://www.bantaypresyo.da.gov.ph/tbl_price_get_comm_header_rice.php"

data = {
    "commodity": "1",
    "region": "130000000"
}

header_response = requests.post(header_url, data=data)
header_soup = BeautifulSoup(header_response.text, "html.parser")

headers = [
    cell.get_text(strip=True)
    for cell in header_soup.find_all(["td", "th"])
]

print("Markets:")
for i, header in enumerate(headers):
    print(i, header)


# 2. Get prices

price_url = "http://www.bantaypresyo.da.gov.ph/tbl_price_get_comm_price_rice.php"

price_response = requests.post(price_url, data=data)
price_soup = BeautifulSoup(price_response.text, "html.parser")

rows = price_soup.find_all("tr")

print("\nFirst commodity:")

cells = rows[1].find_all("td")

commodity = cells[0].get_text(strip=True)
specification = cells[1].get_text(strip=True)

print("Commodity:", commodity)
print("Specification:", specification)

for i in range(2, len(cells)):
    market = headers[i]
    price = cells[i].get_text(strip=True)

    print(market, "=", price)