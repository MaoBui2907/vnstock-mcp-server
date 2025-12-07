from vnstock import Quote
from typing import Literal
from datetime import datetime
from fastmcp import FastMCP
from vnstock_mcp.libs.utils import with_output_format

quote_mcp = FastMCP("Quote")


@with_output_format
def get_quote_history_price(symbol: str, start_date: str, end_date: str = None, interval: Literal['1m', '5m', '15m', '30m', '1H', '1D', '1W', '1M'] = '1D'):
    """
    Get quote price history of a symbol from stock market
    Args:
        symbol: str (symbol to get history price)
        start_date: str (format: YYYY-MM-DD)
        end_date: str = None (end date to get history price. None means today)
        interval: Literal['1m', '5m', '15m', '30m', '1H', '1D', '1W', '1M'] = '1D' (interval to get history price)
    Returns:
        pd.DataFrame
    """
    quote = Quote(symbol=symbol, source='VCI')
    return quote.history(start_date=start_date, end_date=end_date or datetime.now().strftime('%Y-%m-%d'), interval=interval)


@with_output_format
def get_quote_intraday_price(symbol: str, page_size: int = 100, last_time: str = None):
    """
    Get quote intraday price from stock market
    Args:
        symbol: str (symbol to get intraday price)
        page_size: int = 500 (max: 100000) (number of rows to return)
        last_time: str = None (last time to get intraday price from)
    Returns:
        pd.DataFrame
    """
    quote = Quote(symbol=symbol, source='VCI')
    return quote.intraday(page_size=page_size, last_time=last_time)


@with_output_format
def get_quote_price_depth(symbol: str):
    """
    Get quote price depth from stock market
    Args:
        symbol: str (symbol to get price depth)
    Returns:
        pd.DataFrame
    """
    quote = Quote(symbol=symbol, source='VCI')
    return quote.price_depth()


# Register all functions as MCP tools
quote_mcp.tool(get_quote_history_price)
quote_mcp.tool(get_quote_intraday_price)
quote_mcp.tool(get_quote_price_depth)
