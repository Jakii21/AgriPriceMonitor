import requests
from bs4 import BeautifulSoup

url = "http://www.bantaypresyo.da.gov.ph/tbl_price_get_comm_price_rice.php"

data = {
    "commodity": "1",
    "region": "130000000"
}

response = requests.post(url, data=data)

soup = BeautifulSoup(response.text, "html.parser")

rows = soup.find_all("tr")

print("Number of rows:", len(rows))

for row in rows[:5]:
    cells = row.find_all(["td", "th"])
    print([cell.get_text(strip=True) for cell in cells])