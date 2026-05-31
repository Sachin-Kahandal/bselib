from bselib import analysis, gainers, script, quote, statements

class BSE:
    """
    This class implements all the functions for bselib
    """
    def analysis(self, script_code):
        """
        :Returns analysis of price and value for script
        """
        return analysis.analysis(script_code)

    def stmt_analysis(self, script_code, stats):
        """
        :Returns analysis of financial statements
        """
        return analysis.stmt_analysis(script_code, stats)        

    def corporate_actions(self, script_code):
        """
        :Returns info about board meetings, dividends, split, bonus and rights issued
        """
        return quote.corporate_actions(script_code)

    def get_gainers(self):
        """
        :Returns top 5 perfomers of the day
        """
        return gainers.get_gainers()

    def holdings(self, script_code):
        """
        :Returns shareholding pattern and analysis
        """
        return quote.holdings(script_code)

    def index(self):
        """
        :Returns NSE and BSE basic info
        """
        return gainers.get_index()

    def get_losers(self):
        """
        :Returns worst 5 perfomers of the day
        """
        return gainers.get_losers()

    def news(self, script_code):
        """
        :Returns news related to company
        """
        return quote.news(script_code)

    def peers(self, script_code):
        """
        :returns competitors and some info within same sector
        """
        return quote.peers(script_code)

    def comp_profile(self,script_code):
        """
        :Returns info about companies buisness
        """
        return quote.get_profile(script_code)

    def script(self, stock):
        """
        :Returns a script codes for searched stock
        """
        return script.script(stock)

    def quote(self, script_code):
        """
        :Returns basic details about stock like current price, market-cap, high-lows and bulk-deals
        """
        return quote.quote(script_code)

    def bulk_deals(self,script_code):
        """
        financial ratios which can be used to determine the stocks health/value/performance
        """
        return quote.bulk_deals(script_code)

    def ratios(self, script_code):
        """
        :Returns few key financial ratios
        """
        return quote.ratios(script_code)

    def statement(self, script_code, stats):
        """
        :Returns snapshot of recent financial statements
        """
        return statements.statement(script_code, stats)

    def historical_stats(self, script_code, stats):
        """
        :Returns snapshots of historical financial statements
        """
        return statements.historical_stats(script_code, stats)


    def annual_reports(self, script_code):
        """
        Returns links to annual reports
        """
        return statements.annual_reports(script_code)

    def credit_reports(self, script_code):
        """
        :Returns links to credit reports 
        """
        return statements.credit_reports(script_code)

    def __str__(self):
        return 'Driver Class for Bombay Stock Exchange'

    def __repr__(self):
        return 'Driver Class for Bombay Stock Exchange'