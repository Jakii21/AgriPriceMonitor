import requests
from bs4 import BeautifulSoup

url = "http://www.bantaypresyo.da.gov.ph/tbl_price_get_comm_header_rice.php"

data = {
    "commodity": "1",
    "region": "130000000"
}

response = requests.post(url, data=data)

soup = BeautifulSoup(response.text, "html.parser")

cells = soup.find_all(["td", "th"])

for i, cell in enumerate(cells):
    print(i, cell.get_text(strip=True))