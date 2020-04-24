import requests
from bs4 import BeautifulSoup

# BULK DEALS
def bulk(script_code):
    try:
        x = int(script_code)   
        script_code = str(x)
        if len(script_code) == 6:
            baseurl5 = "https://api.bseindia.com/BseIndiaAPI/api/TabResults/w?scripcode="+str(script_code)+"&tabtype=BULK"
            data5 = requests.get(baseurl5)
            bulkDeals = data5.json()
            if len(bulkDeals) == 0:
                bulkDeals = {'info':'error'}
        else:
            msg = {'info':'length of script_code should be 6 digit'}
            return msg
    except:
        msg = {'info':'Error'}
    return bulkDeals