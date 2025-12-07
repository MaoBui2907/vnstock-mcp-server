from vnstock.explorer.fmarket.fund import Fund as FMarketFund
from typing import Literal
from fastmcp import FastMCP
from vnstock_mcp.libs.utils import with_output_format

fund_mcp = FastMCP("Fund")


@with_output_format
def list_all_funds(fund_type: Literal['BALANCED', 'BOND', 'STOCK', None] = None):
    """
    List all funds from stock market
    Args:
        fund_type: Literal['BALANCED', 'BOND', 'STOCK', None ] = None (if None, return funds in all types)
    Returns:
        pd.DataFrame
    """
    fund = FMarketFund()
    return fund.listing(fund_type=fund_type)


@with_output_format
def search_fund(keyword: str):
    """
    Search fund by name from stock market
    Args:
        keyword: str (partial match for fund name to search)
    Returns:
        pd.DataFrame
    """
    fund = FMarketFund()
    return fund.filter(symbol=keyword)


@with_output_format
def get_fund_nav_report(symbol: str):
    """
    Get nav report of a fund from stock market
    Args:
        symbol: str (symbol of the fund to get nav report)
    Returns:
        pd.DataFrame
    """
    fund = FMarketFund()
    return fund.details.nav_report(symbol=symbol)


@with_output_format
def get_fund_top_holding(symbol: str):
    """
    Get top holding of a fund from stock market
    Args:
        symbol: str (symbol of the fund to get top holding)
    Returns:
        pd.DataFrame
    """
    fund = FMarketFund()
    return fund.details.top_holding(symbol=symbol)


@with_output_format
def get_fund_industry_holding(symbol: str):
    """
    Get industry holding of a fund from stock market
    Args:
        symbol: str (symbol of the fund to get industry holding)
    Returns:
        pd.DataFrame
    """
    fund = FMarketFund()
    return fund.details.industry_holding(symbol=symbol)


@with_output_format
def get_fund_asset_holding(symbol: str):
    """
    Get asset holding of a fund from stock market
    Args:
        symbol: str (symbol of the fund to get asset holding)
    Returns:
        pd.DataFrame
    """
    fund = FMarketFund()
    return fund.details.asset_holding(symbol=symbol)


# Register all functions as MCP tools
fund_mcp.tool(list_all_funds)
fund_mcp.tool(search_fund)
fund_mcp.tool(get_fund_nav_report)
fund_mcp.tool(get_fund_top_holding)
fund_mcp.tool(get_fund_industry_holding)
fund_mcp.tool(get_fund_asset_holding)
