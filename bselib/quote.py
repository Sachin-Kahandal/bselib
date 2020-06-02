from bs4 import BeautifulSoup
import requests
import json
from bselib.getId import getScript_id 

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
invalid_script_code = {'info' : 'Not a valid script_code'}
error = {'info' : 'Error'}

def quote(script_code):
    try:  
        # script codes are suppose to be 6 digit integers
        script_code = int(script_code)   
        if len(str(script_code)) == 6:
            baseurl = 'https://m.bseindia.com/StockReach.aspx?scripcd='
            response = requests.get(baseurl + str(script_code), headers=headers)
            soup = BeautifulSoup(response.text,'lxml')
            quote = dict()
            quote['stockName'] = soup.select("span.companyname")[0].text
            if quote['stockName'] != '':
                quote['currentPrice'] = soup.select("span.srcovalue strong")[0].text
                currentPrice = soup.select("span.srcovalue strong")[0].text
                previousClose = soup.select("td#tdpcloseopen.TTRow_right")[0].text.split('/')[0]
                try:
                    if currentPrice > previousClose:
                        change = soup.select("span#spanchangVal.srcovalue")[0].text.split('(')[0].strip()
                        quote['change'] = '+'+change
                        pChange = soup.select("span#spanchangVal.srcovalue")[0].text.split('(')[1].strip()[:-2]
                        quote['pChange'] = '+'+pChange
                    elif currentPrice == previousClose:
                        quote['change'] = soup.select("span#spanchangVal.srcovalue")[0].text.split('(')[0].strip()
                        quote['pChange'] = soup.select("span#spanchangVal.srcovalue")[0].text.split('(')[1].strip()[:-2]
                    else:
                        change = soup.select("span#spanchangVal.srcovalue")[0].text.split('(')[0].strip()
                        quote['change'] = '-'+change
                        pChange = soup.select("span#spanchangVal.srcovalue")[0].text.split('(')[1].strip()[:-2]
                        quote['pChange'] = '-'+pChange

                except IndexError:
                    quote['change'] = "-"
                    quote['pChange'] = "-"
                quote['ltd'] = soup.select("div.companyright span")[0].text

                quote['securityId'] = soup.select("td#tdCShortName.resultleft")[0].text
                quote['scriptCode'] = soup.select("td#tdscripcode.resultleft")[0].text
                quote['group'] = soup.select("td#tdgroup.resultleft")[0].text.split('/')[0].strip()
                quote['index'] = soup.select("td#tdgroup.resultleft")[0].text.split('/')[1].strip()
                quote['faceValue'] = soup.select("td#tdfacevalue.resultleft")[0].text
                # STOCK TRADING
                quote['previousClose'] = soup.select("td#tdpcloseopen.TTRow_right")[0].text.split('/')[0]
                quote['lastOpen'] = soup.select("td#tdpcloseopen.TTRow_right")[0].text.split('/')[1]
                try:
                    quote['daysHigh'] = soup.select("td#tdDHL.TTRow_right")[0].text.split('/')[0]
                    quote['daysLow'] = soup.select("td#tdDHL.TTRow_right")[0].text.split('/')[1]
                except:
                    quote['daysHigh'] = '-'
                    quote['daysLow'] = '-'
                quote['wtdAvgPrice'] = soup.select("td#tdWAp.TTRow_right")[0].text
                quote['totalTradedValue'] = dict()
                quote['totalTradedValue']['in'] = 'Cr'
                quote['totalTradedValue']['value'] = soup.select("td#tdTTV.TTRow_right")[0].text
                quote['totalTradedQty'] = dict()
                quote['totalTradedQty']['in'] = 'Lac'
                quote['totalTradedQty']['value'] = soup.select("td#tdTTQW.TTRow_right")[0].text.split('/')[0]
                quote['twoWeekAvgQty'] = dict()
                try:
                    quote['twoWeekAvgQty']['in'] = 'Lac'
                    quote['twoWeekAvgQty']['value'] = soup.select("td#tdTTQW.TTRow_right")[0].text.split('/')[1]
                except:
                    quote['twoWeekAvgQty']['in'] = '-'
                    quote['twoWeekAvgQty']['value'] = '-'
                quote['mktCap'] = dict()
                quote['mktCap']['in'] = 'Cr'
                quote['mktCap']['value'] = soup.select("tr#trMktCap td.TTRow_right")[0].text.split('/')[0].strip()
                quote['freeFloat'] = dict()
                quote['freeFloat']['in'] = 'Cr'
                quote['freeFloat']['value'] = soup.select("tr#trMktCap td.TTRow_right")[0].text.split('/')[1].strip()



                # # HIGHS AND LOWS: 1-DAY, 1-WEEK, 1-MONTH, 52-WEEK
                baseurl2 = 'https://api.bseindia.com/BseIndiaAPI/api/HighLow/w?Type=EQ&flag=C&scripcode='
                response2 = requests.get(baseurl2 + str(script_code), headers=headers)
                highLow = response2.json()
                a = highLow['Fifty2WkHigh_adj']
                b = highLow['Fifty2WkLow_adj']
                quote['fiftytwo_WeekHigh'] = float(a)
                quote['fiftytwo_WeekLow'] = float(b)
                quote['monthHighLow'] = highLow['MonthHighLow']
            else:
                return invalid_script_code
        else:
            return invalid_script_code
    except:
        return error
    return quote


def bulk_deals(script_code):
    # BULK DEALS
    try:
        # script codes are suppose to be 6 digit integers
        script_code = int(script_code)   
        if len(str(script_code)) == 6:     
            baseurl = "https://api.bseindia.com/BseIndiaAPI/api/TabResults/w?scripcode="+str(script_code)+"&tabtype=BULK"
            response = requests.get(baseurl, headers=headers)
            bulkDeals = response.json()
            if len(bulkDeals) == 0:
                bulkDeals = error
            deals = {'bulk_deals':bulkDeals}
        else:
            return invalid_script_code
    except:
        return error
    return deals


def ratios(script_code):
    try:
        # script codes are suppose to be 6 digit integers
        script_code = int(script_code)   
        if len(str(script_code)) == 6:
        # RATIOS: PE, EPS(TTM), CEPS, PB, ROE, FACEVALUE
            baseurl = "https://api.bseindia.com/BseIndiaAPI/api/ComHeader/w?quotetype=EQ&scripcode="+str(script_code)+"&seriesid="
            response = requests.get(baseurl, headers=headers)
            ratio1 = response.json()
            if (ratio1['SecurityId'] == None):
                return invalid_script_code
            # INFO(52 wk high-low with dates,Revenue,PAT,Equity) RATIOS(OPM,NPM,RONW)
            ratio3 = dict()
            baseurl1 = "https://api.bseindia.com/BseIndiaAPI/api/EQPeerGp/w?scripcode="+str(script_code)+"&scripcomare="
            response1 = requests.get(baseurl1)
            ratio2 = response1.json()
            ratio3['OPM'] = ratio2['Table'][0]['OPM']
            ratio3['NPM'] = ratio2['Table'][0]['NPM']
            ratio3['RONW'] = ratio2['Table'][0]['RONW']
            ratio3['EPS'] = ratio2['Table'][0]['EPS']
            ratio3['CEPS'] = ratio2['Table'][0]['Cash_EPS']
            ratio3['PE'] = ratio2['Table'][0]['PE']
            data = {'value_ratio':ratio1,'profit_ratio':ratio3}
        else:
            return invalid_script_code
    except:
        return error
    return data    


def peers(script_code):
    try:
        # script codes are suppose to be 6 digit integers
        script_code = int(script_code)   
        if len(str(script_code)) == 6:
            # PEER COMPARISON WITH INFO(52 wk high-low with dates,Revenue,PAT,Equity,Shareholdings) 
            # RATIOS(OPM,NPM,RONW,EPS,CEPS,PE)
            baseurl = "https://api.bseindia.com/BseIndiaAPI/api/EQPeerGp/w?scripcode="+str(script_code)+"&scripcomare="
            response = requests.get(baseurl, headers=headers)
            peer_comp = response.json()
            if peer_comp['Table'][0]['scrip_cd'] == None:
                return invalid_script_code
        else:
            return invalid_script_code
    except:
        return error
    return peer_comp


def holdings(script_code):
    try:
        # script codes are suppose to be 6 digit integers
        script_code = int(script_code)   
        if len(str(script_code)) == 6:
            stocks_id = getScript_id(script_code,"id")
            url = 'https://frapi.marketsmojo.com/Stocks_Shareholding/get_results?sid='+str(stocks_id)+'&exchange=0&close_peer=undefined'
            response = requests.get(url, headers=headers)
            mojo_hold = response.json()
            # CLEANING JSON
            holding_data = dict()
            holding_data['holdings'] = mojo_hold['data']["shareholding_snapshot"]
            holding_data['holding_comp'] = mojo_hold['data']["shareholding_compare"]
            holding_data['holding_analysis'] = mojo_hold['data']["shareholding_analysis"]
        else:
            return invalid_script_code
    except:
        return error
    return holding_data


def news(script_code):
    try:
        # script codes are suppose to be 6 digit integers
        script_code = int(script_code)   
        if len(str(script_code)) == 6:
            stocks_id = getScript_id(script_code,"id")
            url = 'https://frapi.marketsmojo.com/Stocks_Priceupdates/priceupdates_info?sid='+str(stocks_id)+'&exchange=0&se=bse&cardlist=sectPrice_techScore&'
            response = requests.get(url, headers=headers)
            news = response.json()
            news_data = dict()
            news_data['news'] = news['data']['NEWS']
        else:
            return invalid_script_code
    except:
        return error
    return news_data


def corporate_actions(script_code):
    try:
        # script codes are suppose to be 6 digit integers
        script_code = int(script_code)   
        if len(str(script_code)) == 6:
            stocks_id = getScript_id(script_code,"id")
            url = 'https://frapi.marketsmojo.com/Stocks_Corporateactions/Corp_action_Full_Details?sid='+str(stocks_id)+'&exchange=0&nores=null&'
            response = requests.get(url,headers=headers)
            corp_act = response.json()
            # CLEANING JSON
            corp_action = dict()
            corp_action['board_meetings'] = corp_act['data'][0]['data'][:3]
            corp_action['dividends'] = corp_act['data'][1]
            corp_action['splits'] = corp_act['data'][2]
            corp_action['bonus'] = corp_act['data'][3]
            corp_action['rights'] = corp_act['data'][4]
        else:
            return invalid_script_code
    except:
        return error
    return corp_action


def get_profile(script_code):
    try:
        # script codes are suppose to be 6 digit integers
        script_code = int(script_code)   
        if len(str(script_code)) == 6:
            data = getScript_id(script_code,"name")  
            yahoo_url = 'https://query1.finance.yahoo.com/v1/finance/search?q='+str(data)+'&quotesCount=6&newsCount=0&enableFuzzyQuery=false&quotesQueryId=tss_match_phrase_query&multiQuoteQueryId=multi_quote_single_token_query&newsQueryId=news_ss_symbols&enableCb=false&enableNavLinks=false&vespaNewsTimeoutMs=600'
            yahoo = requests.get(yahoo_url, headers=headers)
            res = yahoo.json()
            symbol = res['quotes'][0]['symbol']
            profile_url = 'https://in.finance.yahoo.com/quote/'+str(symbol)+'/profile'
            res = requests.get(profile_url, headers=headers)
            soup = BeautifulSoup(res.text,'lxml')
            link = soup.select("div.asset-profile-container div p a")[1].text
            sector = soup.select("div.asset-profile-container div div p span")[1].text
            industry = soup.select("div.asset-profile-container div div p span")[3].text
            comp_name = soup.select("div.asset-profile-container h3")[0].text
            post = soup.select("div section section span")[7].text
            name = soup.select("div section section span")[6].text
            description = soup.select('section p')[2].text
            profile = {'script_code':script_code, 'symbol':symbol, 'Name':comp_name, 'description':description, 
            post:name, 'website':link, 'industry':industry, 'sector':sector}
        else:
            return invalid_script_code
    except:
        return error
    return profile