.. bselib documentation master file, created by
   sphinx-quickstart on Fri Apr 24 13:34:05 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to bselib's documentation!
==================================
Python library for extracting real-time data from Bombay Stock Exchange (India)

Usage
=====

Installing with pip
-------------------

.. code-block:: Bash

    pip install bselib

Instantiation
-------------

.. code-block:: Python

    from bselib.bse import BSE
    b = BSE()
    print(b)
    # Output:
    Driver Class for Bombay Stock Exchange

Getting/Verifying a script code
---------------------
This method takes string/integer as an argument and returns list of stocks results.
You can use pprint() for better view of the json/dict data

.. code-block:: Python 

    stocks = b.get_script('reliance')
    pprint(stocks)
    # Output:
    pprint(stocks)
    {500111: 'Reliance Capital Ltd.',
    500325: 'Reliance Industries Ltd.',
    500390: 'Reliance Infrastructure Ltd.',
    503162: 'Reliance Chemotex Industries Ltd.',
    523445: 'Reliance Industrial Infrastructure Ltd.',
    532703: 'Reliance Capital Ventures (Delisted)',
    532704: 'Reliance Energy Ventures (Delisted)',
    532712: 'Reliance Communications Ltd.',
    533143: 'Reliance Broadcast Network Ltd. (Delisted)',
    540709: 'Reliance Home Finance Ltd.'}
    
    stocks = b.get_script(500325)
    # Output:
    pprint(stocks)
    {500325: 'Reliance Industries Ltd. - 500325'}

Getting a stock quote
---------------------

This method returns current price, detail high-low prices and other info you can pick the fields you require from the dictionary

.. code-block:: Python

    data = b.quote('500325')
   #Output:
    pprint(data)
    {'high_low': {'CktFilter': None,
            'Fifty2WkHigh_adj': '1617.80',
            'Fifty2WkHigh_adjDt': ' (20/12/2019)',
            'Fifty2WkHigh_unadj': '1617.80 (20/12/2019)',
            'Fifty2WkLow_adj': '875.70',
            'Fifty2WkLow_adjDt': ' (23/03/2020)',
            'Fifty2WkLow_unadj': '875.70 (23/03/2020)',
            'MonthHighLow': '1495.00 / 895.80',
            'UnderlyingVal': None,
            'WeekHighLow': '1495.00 / 1164.45'},
        'quote': {'change': '+45.85',
        'daysHigh': '1495.00',
        'daysLow': '1348.00',
        'faceValue': '10.00',
        'freeFloat': {'in': 'Cr', 'value': '4,76,204.94'},
        'group': 'A',
        'index': 'S&P BSE SENSEX',
        'lastOpen': '1354.90',
        'ltd': 'LTD- 24 Apr 20 | 03:59 PM',
        'mktCap': {'in': 'Cr', 'value': '8,98,499.89'},
        'pChange': '+3.34',
        'previousClose': '1371.50',
        'scriptCode': '500325',
        'securityId': 'RELIANCE',
        'stockName': 'RELIANCE INDUSTRIES LTD.',
        'stockPrice': '1417.35',
        'totalTradedQty': {'in': 'Lac', 'value': '24.52'},
        'totalTradedValue': {'in': 'Cr', 'value': '349.89'},
        'twoWeekAvgQty': {'in': 'Lac', 'value': '10.59'},
        'wtdAvgPrice': '1426.94'}}


Getting top gainers
-------------------

.. code-block:: Python

    top_performers = b.get_gainers()
    # Output:
    pprint(top_performers)
    {'gainers': [{'LTP': '96.55',
                   'change': '10.65',
                   'pChange': '12.40',
                   'scriptCode': '500645',
                   'securityID': 'DEEPAKFERT'},
                  {'LTP': '42.95',
                   'change': '3.90',
                   'pChange': '9.99',
                   'scriptCode': '539807',
                   'securityID': 'INFIBEAM'},
                  {'LTP': '225.80',
                   'change': '19.85',
                   'pChange': '9.64',
                   'scriptCode': '532221',
                   'securityID': 'SONATSOFTW'},
                  {'LTP': '181.00',
                   'change': '15.50',
                   'pChange': '9.37',
                   'scriptCode': '500003',
                   'securityID': 'AEGISLOG'},
                  {'LTP': '2,741.00',
                   'change': '220.80',
                   'pChange': '8.76',
                   'scriptCode': '539523',
                   'securityID': 'ALKEM'}]}

Getting top losers
-------------------

.. code-block:: Python

    worst_performer = b.get_losers()
    pprint(worst_performer)
    # Output:
    {'losers': [{'LTP': '216.25',
             'change': '-46.90',
             'pChange': '-17.82',
             'scriptCode': '540767',
             'securityID': 'NAM-INDIA'},
            {'LTP': '132.90',
             'change': '-19.00',
             'pChange': '-12.51',
             'scriptCode': '511243',
            'securityID': 'CHOLAFIN'},
             {'LTP': '314.90',
             'change': '-39.45',
             'pChange': '-11.13',
             'scriptCode': '533273',
             'securityID': 'OBEROIRLTY'},
            {'LTP': '12.66',
             'change': '-1.39',
             'pChange': '-9.89',
             'scriptCode': '532505',
             'securityID': 'UCOBANK'},
            {'LTP': '140.45',
             'change': '-15.30',
             'pChange': '-9.82',
             'scriptCode': '532720',
             'securityID': 'M&MFIN'}]}

         


Getting Financial Statements
----------------------

This function returns a dictionary that can be turned to pandas dataframe.
So it returns quarterly results, balance-sheets, profit-loss statements and cash-flow statements of 10+ years, with links of annual reports of last 5 years and credit reports from CARE, CRISIL and ICRA.
The complete-data returned is to big to be displayed

.. code-block:: Python

    fin = b.stmt(500325)
    

Statement Analysis
--------------------------------------------------
Detail analysis of balance sheets, profit-loss statements, cash-flow statements,
quarter results comparing to last years respective statements.
Output is quite big to be displayed but it will be similar to Performance Analysis. 

.. code-block:: Python

     pa = b.perform_analysis(500325)


Getting Performance Analysis
--------------------------------------------------
Daily basis performance analysis of stock

.. code-block:: Python

    pa = b.performance_analysis(500325)
    # Output: 

    {'analysis': [{'dir': 1,
               'header': 'Performance Today',
               'msg': 'Outperformed Sector by 1.16%'},
              {'dir': 1,
               'header': 'Consecutive Gain',
               'msg': 'Stock has been gaining for the last 3 days and has '
                       'risen 14.52% returns in the period'},
              {'dir': 1,
               'header': "Day's High",
               'msg': 'Stock touched an intraday high of Rs 1494.95 (9.05%)'},
              {'dir': 0,
               'header': 'Wide Range',
               'msg': 'The stock has traded in a wide range of Rs 147.75'},
              {'dir': -1,
               'header': 'Weighted Average Price',
               'msg': 'More Volume traded close to Low Price'},
              {'dir': 1,
               'header': 'Moving Averages',
               'msg': 'Reliance Industries is trading higher than 5 day, 20 '
                      'day, 50 day, 100 day and 200 day moving averages'},
              {'dir': 1,
               'header': 'Action in Sector',
               'msg': 'Oil Exploration/Refineries has gained by 2.2%'},
              {'dir': -1,
               'header': 'Falling Investor Participation',
               'msg': 'Delivery Vol of 28.78 lacs on 13 Apr has fallen by '
                      '-65.77% against 5-day avg delivery vol '},
              {'dir': 0,
               'header': 'Liquidity',
               'msg': 'Based on 2% of 5 day average traded Value the stock is '
                      'liquid enough for trade size of Rs 83.78 cr'}]
.. note::    dir: 1 - denotes positive point,
                  -1 - denotes negative point, 0 - Neutral point

Getting Financial Ratios
--------------------------------------------------
PE, EPS, CEPS, PB, ROE, OPM, NPM, RONW, and info like Face-value, Revenue and PAT

.. code-block:: Python

    ratios = b.ratios(500325)


Getting peers comparisons
--------------------------------------------------

Peer comparison with info (52 wk high-low with dates,Revenue,PAT,Equity,Shareholdings) 
and ratios (OPM,NPM,RONW,EPS,CEPS,PE)

.. code-block:: Python

    peers = b.ratios(500325)

Getting corporate News
--------------------------------------------------
News related to corporate

.. code-block:: Python

    peers = b.ratios(500325)

    # Output:
    {'news': [{'description': "Market LIVE: Indices off day's lows; Reliance "
                          'Industries surges 6%  Livemint',
           'entts': 1587735001,
           'imagepath': '',
           'isdeleted': 0,
           'link': 'https://www.livemint.com/market/live-blog/live-blog-sensex-nifty-live-today-24-04-2020-nifty-nse-bse-news-updates-11587696877586.html',
           'newsid': '274655611f3cc7d430a4bafffed1208a',
           'newstype': 'STKNWS',
           'publisheddate': '24-Apr-2020 08:34',
           'source': 'https://www.livemint.com',
           'title': "Market LIVE: Indices off day's lows; Reliance Industries "
                    'surges 6%',
           'topnews': 0},
          {'description': 'Reliance Jio & Facebook differ on key issues  '
                          'Economic Times',
           'entts': 1587733201,
           'imagepath': '',
           'isdeleted': 0,
           'link': 'https://economictimes.indiatimes.com/tech/internet/reliance-jio-facebook-differ-on-key-issues/articleshow/75334079.cms',
           'newsid': 'c037eec91e7df3d3db10a819600ac3d1',
           'newstype': 'STKNWS',
           'publisheddate': '24-Apr-2020 16:48',
           'source': 'https://economictimes.indiatimes.com',
           'title': 'Reliance Jio & Facebook differ on key issues',
           'topnews': 0},
          {'description': 'Amazon doubles down on small sellers with new '
                          'scheme amid Reliances plan to build grocery '
                          'powerhouse  The Financial Express',
           'entts': 1587666601,
           'imagepath': '',
           'isdeleted': 0,
           'link': 'https://www.financialexpress.com/industry/sme/msme-tech-amazon-doubles-down-on-small-sellers-with-new-scheme-amid-reliances-plan-to-build-grocery-powerhouse/1937822/',
           'newsid': '33730b41d9d3ddaa4fc1cb6c6f593a9f',
           'newstype': 'STKNWS',
           'publisheddate': '23-Apr-2020 19:18',
           'source': 'https://www.financialexpress.com',
           'title': 'Amazon doubles down on small sellers with new scheme amid '
                    'Reliances plan to build grocery powerhouse',
           'topnews': 0}]}


Getting Corporate's business information
--------------------------------------------------
.. code-block:: Python

    info = b.comp_details(500325)
    # Output:
    {'info': {'about_the_company': "Reliance Industries Ltd  is India's largest private 
    sector enterprise, with businesses in the energy and materials value chain.The 
    company works under different business segments:Exploration and Production,Petroleum 
    Refining and Marketing,Petrochemicals,Textiles and Retail.Products and brands offered 
    by the company includes:Crude oil and natural 
    gas,LPG,Propylene,Naphtha,Gasoline,Jet/Aviation Turbine Fuel,Superior Kerosene 
    Oil,High Speed Diesel,Sulphur,Petroleum Coke,Polypropylene,High Density 
    Polyethylene,Low Density Polyethylene,Linear Low
    Density Polyethylene,Polyvinyl Chloride,Poly –Olefin,Suitings ,Shirtings,Readymade 
    Garments,Furnishing fabrics,Day curtains,Automotive upholstery,Suitings,Ready-to- 
    stitch,Take away fabric,Fleet management services,Highway hospitality 
    services,Vehicle care services,Linear Alkyl Benzene,Paraxylene,Purified Terephthalic 
    Acid,Mono Ethylene Glycol,Staple Fibre,Filament Yarn,Texturised yarn,Twisted 
    yarn,Moisture management yarn,Quality certified sleep products & Polyethylene 
    terephthalate.", 'msg': ''}}

Getting Corporate's actions
--------------------------------------------------
Corporate actions include board meetings, declaring things like bonus, dividends, splits and rights

.. code-block:: Python

     data = b.corporate_actions(500325)

Getting Shareholding information and analysis
--------------------------------------------------
.. code-block:: Python

    data = b.holdings(500325)


Getting Bulk deal information
--------------------------------------------------
.. code-block:: Python

    data = b.bulk(500325)
    #Output:
    [{"DealDate":"27/03/2020","Type":"B","Qty":"76735388","Rate":"1056.00","TO":"8103.26"},
    {"DealDate":"27/03/2020","Type":"S","Qty":"86552244","Rate":"1056.61","TO":"9145.20"},
    {"DealDate":"25/03/2020","Type":"B","Qty":"116081170","Rate":"949.50","TO":"11021.91"},
    {"DealDate":"25/03/2020","Type":"S","Qty":"116081170","Rate":"949.50","TO":"11021.91"}]
