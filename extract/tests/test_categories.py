import requests

url = "http://www.bantaypresyo.da.gov.ph/tbl_price_get_comm_price_meat.php"

commodities = {
    "Fruits": "5",
    "Highland Vegetables": "6",
    "Lowland Vegetables": "7",
    "Meat and Poultry": "8"
}

for name, commodity_id in commodities.items():

    data = {
        "commodity": commodity_id,
        "region": "130000000"
    }

    response = requests.post(url, data=data)

    print("\n==============================")
    print(name)
    print("Status:", response.status_code)
    print("Response length:", len(response.text))
    print(response.text[:300])