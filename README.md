# bselib

Python library for extracting real-time data from Bombay Stock Exchange (India).

## Introduction

bselib is a library that collects real-time data from Bombay Stock Exchange (India) and 
historical data from some other sites. It can be used in various types of projects which 
require getting live quotes, historical data at some extent, corporate news and their actions,
ratios, financial statements, credit reports and analysis. Stock simulator and Portfolio management for an example 

The quote is as accurate as provided on the [BSE website](m.bseindia.com).

> **Please do not use this application for production usage. It is best used for learning and building application for your own use. For commercial application you better buy a data service.**
>
> **This library uses MIT license hence liability lies with the user and not the author of the application.**


## Features:

* Getting live quotes using companies script codes.
* Getting script codes by search.
* Getting list of top gainers and losers.
* Getting quotes for all the stocks listed on BSE.
* Getting historical summary of corporate's quarterly results, balance sheets, profit-loss and cash-flow statements.
* Getting analysis of finacial statements, quarterly and  annual results, balacesheets and cashflows. 
* Getting information about corporate's board meetings, dividends, bonus, splits, and rights issued.
* Getting links of credit reports from ICRA and CARE rating agencies.
* Getting corporate's shareholding information.
* Getting corporate's and it's peer's comparisons.
* Getting links of histoarical annual results.
* Getting news related to corporate.
* Getting different financial ratios of corporate.
* Getting analysis regarding corporates performance and valuation. 
* Getting corporates basic business information.

## Usage

Refer the documentation at https://bselib.readthedocs.io/en/latest/

## Dependencies

* [BeautifulSoup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [Requests](http://docs.python-requests.org/en/master/)
* [Pandas](https://pandas.pydata.org/docs/index.html)
* [Html5lilb](https://html5lib.readthedocs.io/en/latest/)
* A fast internet connection.

## License

MIT License

Copyright (c) 2020 Sachin Kahandal

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
 
