from bs4 import BeautifulSoup
import requests


def get_losers():
    baseurl = 'https://m.bseindia.com'
    html = requests.get(baseurl)
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
        except:
            msg = {'info':'Error'}
            return msg
    data = {'losers':losers}
    return data