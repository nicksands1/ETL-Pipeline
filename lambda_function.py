import json
import csv
import requests
import boto3


coin_list = ['bitcoin', 'ethereum', 'tether', 'solana', 'cardano', 'ripple', 'litecoin', 'dogecoin', 'polygon', 'stellar']
url = "https://api.coincap.io/v2/assets"
payload = {"ids" : ','.join(coin_list)}
coins=[]
header=['SYMBOL', 'NAME', 'PRICE', 'SUPPLY', '% CHANGE', 'MARKET CAP']
bucket = 'hold-data'


def lambda_handler(event, context):
    response = requests.request("GET", url, params=payload)
    response = response.json()
    for x in response['data']:
        listing = [x['symbol'],x['name'],x['priceUsd'],x['supply'],x['changePercent24Hr'],x['marketCapUsd']]
        coins.append(listing)
  
    with open('/tmp/crypto.csv', 'w', encoding="UTF-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(coins)

    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(Filename = '/tmp/crypto.csv', Bucket= bucket, Key = 'crypto.csv')

    print('Upload Done')
