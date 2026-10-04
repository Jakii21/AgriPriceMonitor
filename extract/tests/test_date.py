import requests

url = "http://www.bantaypresyo.da.gov.ph/tbl_rice.php"

data = {
    "action": "get_latest_date",
    "region": "130000000",
    "commodity": "1"
}

response = requests.post(url, data=data)

print("Status:", response.status_code)
print("Date:", response.text.strip())