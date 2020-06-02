from bs4 import BeautifulSoup
import requests
import json


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
error = {'info' : 'Error'}

def get_gainers():
    baseurl = 'https://m.bseindia.com'
    html = requests.get(baseurl, headers=headers)
    soup = BeautifulSoup(html.text, "lxml")

    gainers = []
    # 5 TOP_GAINERS
    for i in range(2,7):
        try: 
            gainer = {"securityID": soup.select("div#divGainers tr:nth-of-type("+str(i)+") a.announcelink")[0].text,
            "scriptCode": str(soup.select("div#divGainers tr:nth-of-type("+str(i)+") a")[0]).split('?')[1].split('"')[0].split('=')[1], 
            "LTP": soup.select("div#divGainers tr:nth-of-type("+str(i)+") td.TTRow_right:nth-of-type(2)")[0].text, 
            "change": soup.select("div#divGainers tr:nth-of-type("+str(i)+") td.TTRow_right:nth-of-type(3)")[0].text, 
            "pChange": soup.select("div#divGainers tr:nth-of-type("+str(i)+") td.TTRow_right:nth-of-type(4)")[0].text}
            gainers.append(gainer)
        except:
            return error
    data = {'gainers':gainers}
    return data

def get_losers():
    baseurl = 'https://m.bseindia.com'
    html = requests.get(baseurl, headers=headers)
    soup = BeautifulSoup(html.text, "lxml")

    losers = []
    # 5 TOP LOSERS
    for i in range(2,7):
        try:
            loser = {"securityID": soup.select("div#divLosers tr:nth-of-type("+str(i)+") td.TTRow_left")[0].text,
            "scriptCode": str(soup.select("div#divLosers tr:nth-of-type("+str(i)+") a")[0]).split('?')[1].split('"')[0].split('=')[1], 
            "LTP": soup.select("div#divLosers tr:nth-of-type("+str(i)+") td.TTRow_right:nth-of-type(2)")[0].text, 
            "change": soup.select("div#divLosers tr:nth-of-type("+str(i)+") td.TTRow_right:nth-of-type(3)")[0].text, 
            "pChange": soup.select("div#divLosers tr:nth-of-type("+str(i)+") td.TTRow_right:nth-of-type(4)")[0].text}
            losers.append(loser)
            data = {'losers':losers}
        except:
            return error
    return data

def get_index():
    # API-CALL TO GET NSE MARKET STATUS
    try:
        nse_url = 'https://www.nseindia.com/api/marketStatus'
        nse_market_status = requests.get(nse_url, headers=headers)
        nse_status = nse_market_status.json()
        nse_status = nse_status['marketState'][0]
    except:
        nse_status = {'nse_info':'Error'}

    # API-CALL TO GET BSE MARKET STATUS
    try:
        bse_url = 'https://api.bseindia.com/bseindia/api/Sensex/getSensexData?json={"fields":"1,2,3,4,5,6"}'
        bse_market_status = requests.get(bse_url, headers=headers)
        bse_status = bse_market_status.json()
    except:
        bse_status = {'bse_info':'Error'}
    
    return nse_status, bse_status