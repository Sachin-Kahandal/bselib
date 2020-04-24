import requests 


headers = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
    'Referer' : 'https://www.screener.in/login/'
}
def get_index():
    # API-CALL TO GET NSE MARKET STATUS
    try:
        nse_url = 'https://www.nseindia.com/api/marketStatus'
        nse_market_status = requests.get(nse_url, headers=headers)
        nse_status = nse_market_status.json()
        nse_status = nse_status['marketState'][0]
    except:
        nse_status = {'info':'Error'}

    # API-CALL TO GET BSE MARKET STATUS
    try:
        bse_url = 'https://api.bseindia.com/bseindia/api/Sensex/getSensexData?json={"fields":"1,2,3,4,5,6"}'
        bse_market_status = requests.get(bse_url, headers=headers)
        bse_status = bse_market_status.json()
    except:
        bse_status = {'info':'Error'}
    
    return nse_status, bse_status