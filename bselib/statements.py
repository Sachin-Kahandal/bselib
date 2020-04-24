from bs4 import BeautifulSoup
import requests
from pandas import read_html


def stmts(script_code):
    try:
        x = int(script_code)   
        script_code = str(x)
        if len(script_code) == 6:
            baseurl = 'https://www.screener.in/api/company/search/?q='
            url = (baseurl + script_code)
            urlreq = requests.get(url)
            stocks = urlreq.json()
            screener_url = stocks[0]['url']
            if len(screener_url) == 0: 
                msg = {'info' : 'incoorect script_code'}
                return msg
            dope = ('https://www.screener.in'+str(screener_url)) 
            res = requests.get(dope)
            soup = BeautifulSoup(res.content, 'lxml')

            df = read_html(dope,index_col=None)

            # QUARTERLY RESULTS
            quarter_res = df[0].to_dict()
            # PROFIT-LOSS STATEMENTS
            pl_stats = df[1].to_dict()
            # BALANCESHEETS
            bal_sheets = df[6].to_dict()
            # CASHFLOW
            cashf_stats = df[7].to_dict()
            statements = {'quarter_results':quarter_res, 'profit-loss_stats':pl_stats, 'balancesheets':bal_sheets,
            'cashflow_stats':cashf_stats}

            # ANNUAL REPORT LINKS
            link_text, links, data, data_text = list(), list(), list(), list()
            for j in range(1,6):
                for link in soup.select("div.three:nth-of-type(2) li:nth-of-type("+str(j)+") a"):
                    data = (link['href'])
                    links.append(data)
                    data_text = link.text.strip().replace("\n","")
                    link_text.append(data_text)
            annual_reports =  dict(zip(link_text, links))

            # CREDIT-RATINGS REPORT LINKS
            link_text, links, data, data_text, count = list(), list(), list(), list(), int()
            count = len(soup.select("div.three:nth-of-type(3) a"))
            for j in range(1,count+1):
                for link in soup.select("div.three:nth-of-type(3) li:nth-of-type("+str(j)+") a"):
                    data = (link['href'])
                    links.append(data)
                    data_text = link.text.strip().replace("\n","")
                    link_text.append(data_text)
            credit_ratings = dict(zip(link_text, links))

            data = {'statements':statements, 'annual_reports':annual_reports, 'credit_ratings':credit_ratings}
            return data
        else:
            msg = {'info':'length of script_code should be 6 digit'}
            return msg
    except:
        msg = {'info' : 'Error'}
        return msg
