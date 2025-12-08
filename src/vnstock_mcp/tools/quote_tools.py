from vnstock import Quote
from typing import Literal
from datetime import datetime
from fastmcp import FastMCP
from vnstock_mcp.libs.utils import with_output_format
from vnstock_mcp.libs.ta_utils import add_indicator, get_available_indicators, get_indicator_info

quote_mcp = FastMCP("Quote")



@with_output_format
def get_quote_price_with_indicators(symbol: str, indicators: list[str], start_date: str, end_date: str = None, interval: Literal['1m', '5m', '15m', '30m', '1H', '1D', '1W', '1M'] = '1D'):
    """
    Get quote price with indicators of a symbol from stock market.
    
    Indicators can be specified with or without parameters:
    - Simple: "rsi", "macd", "stochastic"
    - With params: "rsi(window=21)", "macd(fast=12, slow=26, signal=9)"
    
    Args:
        symbol: str (symbol to get price)
        indicators: list[str] (list of indicators with optional parameters)
            Examples:
            - ["rsi", "macd"] - use default parameters
            - ["rsi(window=21)", "macd(fast=12, slow=26)"] - custom parameters
            - ["stochastic(k=14, d=3)", "cci(window=20)"] - mixed
        start_date: str (format: YYYY-MM-DD)
        end_date: str = None (end date to get price. None means today)
        interval: Literal['1m', '5m', '15m', '30m', '1H', '1D', '1W', '1M'] = '1D' (interval to get price)
    Returns:
        pd.DataFrame with OHLCV data and requested indicator columns
    """
    quote = Quote(symbol=symbol, source='VCI')
    data = quote.history(start=start_date, end=end_date or datetime.now().strftime('%Y-%m-%d'), interval=interval)
    for indicator in indicators:
        data = add_indicator(data, indicator)
    return data

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
    return quote.history(start=start_date, end=end_date or datetime.now().strftime('%Y-%m-%d'), interval=interval)


@with_output_format
def get_quote_intraday_price(symbol: str, page_size: int = 100, page: int = 1):
    """
    Get quote intraday price from stock market
    Args:
        symbol: str (symbol to get intraday price)
        page_size: int = 500 (max: 100000) (number of rows to return)
        page: int = 1 (page number to get intraday price from)
    Returns:
        pd.DataFrame
    """
    quote = Quote(symbol=symbol, source='VCI')
    return quote.intraday(page_size=page_size, page=page)


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


def _get_available_indicators_detailed():
    """
    Get list of all available indicators with detailed information.
    Returns list of dicts with name, description, parameters, output_columns, and usage.
    """
    return get_available_indicators(detailed=True)

def _list_available_indicators():
    """
    List all available indicators.
    Returns list of dicts with name, description, parameters, output_columns, and usage.
    """
    return get_available_indicators()


# Register all functions as MCP tools
quote_mcp.tool(get_quote_price_with_indicators)
quote_mcp.tool(get_quote_history_price)
quote_mcp.tool(get_quote_intraday_price)
quote_mcp.tool(get_quote_price_depth)

# Resources
quote_mcp.resource("ta://indicators/names")(_list_available_indicators)
quote_mcp.resource("ta://indicators/detailed")(_get_available_indicators_detailed)
quote_mcp.resource("ta://indicators/{indicator}/info")(get_indicator_info)