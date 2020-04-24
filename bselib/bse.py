from bselib import analysis, corporate, gainers, script, holdings, index, bulk
from bselib import kyc, losers, news, peers, quote, ratios, statements, stmt_analysis

class BSE:
    """
    This class implements all the functions for bselib
    """
    def get_script(self, stock):
        """
        :Returns a script codes for searched stock
        """
        return script.get_script(stock)

    def performance_analysis(self, script_code):
        """
        :Returns analysis of prices and value for script
        """
        return analysis.performance_analysis(script_code)

    def corporate_actions(self, script_code):
        """
        :Returns info about board meetings, dividends, split, bonus and rights issued
        """
        return corporate.corporate_actions(script_code)

    def get_gainers(self):
        """
        :Returns top 5 perfomers of the day
        """
        return gainers.get_gainers()

    def holdings(self, script_code):
        """
        :Returns shareholding pattern and analysis
        """
        return holdings.holdings(script_code)

    def index(self):
        """
        :Returns NSE and BSE basic info
        """
        return index.get_index()
    
    def comp_details(self,script_code):
        """
        :Returns info about companies buisness
        """
        return kyc.comp_details(script_code)

    def get_losers(self):
        """
        :Returns worst 5 perfomers of the day
        """
        return losers.get_losers()

    def news(self, script_code):
        """
        :Returns news related to company
        """
        return news.news(script_code)

    def peers(self, script_code):
        """
        :returns competitors and some info within same sector
        """
        return peers.peers(script_code)

    def quote(self, script_code):
        """
        :Returns basic details about stock like current price, market-cap, high-lows and bulk-deals
        """
        return quote.quote(script_code)

    def ratios(self, script_code):
        """
        financial ratios which can be used to determine the stocks health/value/performance
        """
        return ratios.ratios(script_code)

    def stmts(self, script_code):
        """
        :Returns snapshots of historical financial statements with links to annual reports and credit reports
        """
        return statements.stmts(script_code)

    def stmt_analysis(self, script_code):
        """
        :Returns analysis of financial stattements
        """
        return stmt_analysis.stmt_analysis(script_code)

    def bulk(self,script_code):
        """
        :Returns bulk deals done in recent past
        """
        return bulk.bulk(script_code)

    def __str__(self):
        return 'Driver Class for Bombay Stock Exchange'

    def __repr__(self):
        return 'Driver Class for Bombay Stock Exchange'