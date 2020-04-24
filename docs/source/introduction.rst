Introduction
============

bselib is a library for collecting real-time data from Bombay Stock Exchange (India) and 
historical data from some other sites. It can be used in various types of projects which 
require getting live quotes, historical data at some extent, corporate news and their actions,
ratios, financial statements, credit reports and analysis for projects like portfolio management, 
stocks simulator and data analysis. 

.. note::

    The data provided by APIs is only as correct as provided on https://m.bseindia.com

.. warning::

    If you face any issue with the APIs, please report the issue at https://github.com/Sachin-Kahandal/bselib/issues 
    it might be something with the change in the way BSE reports its live quotes. 


Features
--------

* Getting live quotes using companies script codes.
* Getting script codes by search.
* Getting list of top gainers and losers.
* Getting quotes for all the stocks listed on BSE.
* Getting historical summary of corporate's quarterly results, balance sheets, profit-loss and cash-flow statements.
* Getting analysis of finacial statements, quarterly and  annual results. 
* Getting information about corporate's board meetings, dividends, bonus, splits, and rights issued.
* Getting links of credit reports from ICRA and CARE rating agencies.
* Getting corporate's shareholding information.
* Getting corporate's and it's peer's comparisons.
* Getting links of histoarical annual results.
* Getting news related to corporate.
* Getting different financial ratios of corporate.
* Getting analysis regarding corporates performance and valuation. 
* Getting corporates basic business information.

Roadmap
-------

* Get details of an individual index
* Complete unit test coverage
* Daily OHLCV data
* Historical EOD OHLCV data

Dependencies
------------

* BeautifulSoup 4
* Requests
* Pandas
* Html5lib
* JSON
* A working internet connection 

.. warning::

    This library requires an internet connection and correct script-code.
    It will simply return error, in such case check your internet connection, 
    script code you passed.
