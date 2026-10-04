import requests
from bs4 import BeautifulSoup


BASE_URL = "http://www.bantaypresyo.da.gov.ph"

REGION = "130000000"

COMMODITIES = {
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


for commodity_id, info in COMMODITIES.items():

    print("\n====================================")
    print(info["name"])
    print("====================================")

    # GET HEADERS

    header_url = BASE_URL + info["header_endpoint"]

    data = {
        "commodity": commodity_id,
        "region": REGION
    }

    response = requests.post(header_url,data=data)

    soup = BeautifulSoup(response.text,"html.parser")

    headers = []

    for cell in soup.find_all(["td", "th"]):
        headers.append(cell.get_text(strip=True))

    # GET PRICE ROWS

    price_url = BASE_URL + info["price_endpoint"]

    response = requests.post(price_url, data=data)

    soup = BeautifulSoup(response.text,"html.parser")

    rows = soup.find_all("tr")

    # COMPARE POSITIONS

    print("Number of headers:", len(headers))
    print("Number of price rows:", len(rows))

    for row in rows[:3]:

        cells = row.find_all("td")

        if len(cells) < 3:
            continue

        commodity = cells[0].get_text(strip=True)

        print("\nCommodity:", commodity)

        for i in range(2, min(len(cells), 8)):

            market = headers[i]
            price = cells[i].get_text(strip=True)

            print("Position:",i,"| Market:",market,"| Price:",price)