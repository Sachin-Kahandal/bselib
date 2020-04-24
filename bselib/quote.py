from bs4 import BeautifulSoup
import requests


def quote(script_code):
    try:  
        script_code = str(script_code)
        if len(script_code) == 6:
            baseurl = 'https://m.bseindia.com/StockReach.aspx?scripcd='
            html = requests.get(baseurl + script_code)
            soup = BeautifulSoup(html.text,'lxml')
            quote = dict()

            quote['stockName'] = soup.select("span.companyname")[0].text
            if quote['stockName'] != '':
                quote['stockPrice'] = soup.select("span.srcovalue strong")[0].text
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


                # HIGHS AND LOWS: 1-DAY, 1-WEEK, 1-MONTH, 52-WEEK
                baseurl2 = 'https://api.bseindia.com/BseIndiaAPI/api/HighLow/w?Type=EQ&flag=C&scripcode='
                data2 = requests.get(baseurl2 + str(script_code))
                highLow = data2.json()
                if highLow['Fifty2WkHigh_adj'] == None:
                    highLow = {'info' : 'Error'}
                
                data = {'quote':quote, 'high_low':highLow}
                return data
            else:
                msg = {'info' : 'Not a valid script_code'}
                return msg
        else:
            msg = {'info' : 'length of script_code should be 6 digits'}
            return msg
    except:
        msg = {'info' : 'Error'}
        return msg