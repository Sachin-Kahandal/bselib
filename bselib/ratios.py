import requests
from bs4 import BeautifulSoup


def ratios(script_code):
    try:
        x = int(script_code)   
        script_code = str(x)
        if len(script_code) == 6:
        # RATIOS: PE, EPS, CEPS, PB, ROE, FACEVALUE
            baseurl1 = "https://api.bseindia.com/BseIndiaAPI/api/ComHeader/w?quotetype=EQ&scripcode="+str(script_code)+"&seriesid="
            data1 = requests.get(baseurl1)
            ratio1 = data1.json()
            if (ratio1['SecurityId'] == None):
                ratio1 = {'info':'incorrect scritp_code'}
                return ratio1
            # INFO(52 wk high-low with dates,Revenue,PAT,Equity) RATIOS(OPM,NPM,RONW)
            baseurl7 = "https://api.bseindia.com/BseIndiaAPI/api/EQPeerGp/w?scripcode="+str(script_code)+"&scripcomare="
            data7 = requests.get(baseurl7)
            ratio2 = data7.json()
            ratio2 = ratio2['Table'][0]
            data = {'value_ratio':ratio1,'profit_ratio':ratio2}
            return data
        else:
            msg = {'info':'length of script_code should be 6 digit'}
            return msg
    except:
        msg = {'info' : 'Error'}
        return msg