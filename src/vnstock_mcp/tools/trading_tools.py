from vnstock.explorer.vci.trading import Trading as VCITrading
from fastmcp import FastMCP
from vnstock_mcp.libs.utils import with_output_format

trading_mcp = FastMCP("Trading")


@with_output_format
def get_price_board(symbols: list[str]):
    """
    Get price board from stock market
    Args:
        symbols: list[str] (list of symbols to get price board)
    Returns:
        pd.DataFrame
    """
    trading = VCITrading()
    return trading.price_board(symbols_list=symbols)


# Register all functions as MCP tools
trading_mcp.tool(get_price_board)
