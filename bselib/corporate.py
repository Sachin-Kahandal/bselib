import requests 
import json

def corporate_actions(script_code):
    try:
        x = int(script_code)   
        script_code = str(x)
        if len(script_code) == 6:
            mojo_url = 'https://www.marketsmojo.com/portfolio-plus/frontendsearch?SearchPhrase='
            stocks_data = requests.get(mojo_url + script_code)
            stocks = json.loads(stocks_data.text.replace("<b>", "").replace("</b>", "").replace("\t", "").replace("\n", ""))
            if len(stocks) == 0: 
                msg = {'info': 'incorrect script_code'}
            stock_id = (stocks[0]['Id'])
            stocks_id = str(stock_id)
            mojo = requests.get('https://frapi.marketsmojo.com/Stocks_Corporateactions/Corp_action_Full_Details?sid='+str(stocks_id)+'&exchange=0&nores=null&')
            mojo_data = mojo.json()
            # CLEANING JSON
            board_meetings = mojo_data['data'][0]['data'][:3]
            dividends = mojo_data['data'][1]
            splits = mojo_data['data'][2]
            bonus = mojo_data['data'][3]
            rights = mojo_data['data'][4]
            data = {'board_meetings':board_meetings,'dividends':dividends,'splits':splits,'bonus':bonus,'rights':rights}
            return data
        else:
            msg = {'info':'length of script_code should be 6 digit'}
            return msg
    except:
        msg = {'info':'Error'}
        return msg