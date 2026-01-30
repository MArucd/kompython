import requests

payload = { 
    'api_key': '6e6c896984e54d8325a00011308650bf', 
    'url': 'https://www.askona.ru/krovati/krovat-alfa-pm.htm', 
    'render': 'true'  # JS-рендеринг
}
r = requests.get('https://api.scraperapi.com/', params=payload)

print(r.text) 