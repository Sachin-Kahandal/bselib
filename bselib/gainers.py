from bs4 import BeautifulSoup
import requests

def get_gainers():
    baseurl = 'https://m.bseindia.com'
    html = requests.get(baseurl)
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
            msg = {'info':'Error'}
            return msg
    data = {'gainers':gainers}
    return data