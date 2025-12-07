from vnstock.explorer.misc.gold_price import sjc_gold_price, btmc_goldprice
from vnstock.explorer.misc.exchange_rate import vcb_exchange_rate
from typing import Literal
from datetime import datetime
from fastmcp import FastMCP
from vnstock_mcp.libs.utils import with_output_format

misc_mcp = FastMCP("Misc")


@with_output_format
def get_gold_price(date: str = None, source: Literal['SJC', 'BTMC'] = 'SJC'):
    """
    Get gold price from stock market
    Args:
        date: str = None (if None, return today's price. Format: YYYY-MM-DD)
        source: Literal['SJC', 'BTMC'] = 'SJC' (source to get gold price)
    Returns:
        pd.DataFrame
    """
    if date:
        return sjc_gold_price(date=date)
    else:
        return sjc_gold_price() if source == 'SJC' else btmc_goldprice()


@with_output_format
def get_exchange_rate(date: str = None):
    """
    Get exchange rate of all currency pairs from stock market
    Args:
        date: str = None (if None, return today's price. Format: YYYY-MM-DD)
    Returns:
        pd.DataFrame
    """
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')
    return vcb_exchange_rate(date=date)


# Register all functions as MCP tools
misc_mcp.tool(get_gold_price)
misc_mcp.tool(get_exchange_rate)
