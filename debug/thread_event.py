import requests
import json

url = "https://mp-prod.smartmidea.net/mas/v5/app/proxy?alias=/v1/user/login/id/get"

payload = json.dumps({
    "loginAccount": "17328565609",
    "reqId": "ga1a838aad7c85992b71bg3f717975d9",
    "stamp": "1683621785168"
})
headers = {
    'User-Agent': 'Apifox/1.0.0 (https://www.apifox.cn)',
    'Content-Type': 'application/json',
    'sign': 'fc57d8c8c9cff3f07adaf9eaf78ed6b1',
    'random': '0.9236182574629128',
    'Accept': '*/*',
    'Cache-Control': 'no-cache',
    'Host': 'mp-prod.smartmidea.net',
    'Connection': 'keep-alive',
    'Cookie': 'acw_tc=2f61f26116836217722087218e2d7e5b0a8b4d17b5c5b4d67e77a990421536'
}
proxy = {'http': '10.8.68.32:8888', 'https': '10.8.68.32:8888'}
response = requests.request("POST", url, headers=headers, data=payload, proxies=proxy)

print(response.text)
