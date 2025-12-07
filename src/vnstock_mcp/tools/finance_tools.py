from vnstock.explorer.vci.financial import Finance as VCIFinance
from typing import Literal
from fastmcp import FastMCP
from vnstock_mcp.libs.utils import with_output_format

finance_mcp = FastMCP("Finance")


@with_output_format
def get_income_statements(symbol: str, period: Literal['quarter', 'year'] = 'year'):
    """
    Get income statements of a company from stock market
    Args:   
        symbol: str (symbol of the company to get income statements)
        period: Literal['quarter', 'year'] = 'year' (period to get income statements)
    Returns:
        pd.DataFrame
    """
    finance = VCIFinance(symbol=symbol, period=period)
    return finance.income_statement()


@with_output_format
def get_balance_sheets(symbol: str, period: Literal['quarter', 'year'] = 'year'):
    """
    Get balance sheets of a company from stock market
    Args:
        symbol: str (symbol of the company to get balance sheets)
        period: Literal['quarter', 'year'] = 'year' (period to get balance sheets)
    Returns:
        pd.DataFrame
    """
    finance = VCIFinance(symbol=symbol, period=period)
    return finance.balance_sheet()


@with_output_format
def get_cash_flows(symbol: str, period: Literal['quarter', 'year'] = 'year'):
    """
    Get cash flows of a company from stock market
    Args:
        symbol: str (symbol of the company to get cash flows)
        period: Literal['quarter', 'year'] = 'year' (period to get cash flows)
    Returns:
        pd.DataFrame
    """
    finance = VCIFinance(symbol=symbol, period=period)
    return finance.cash_flow()


@with_output_format
def get_finance_ratios(symbol: str, period: Literal['quarter', 'year'] = 'year'):
    """
    Get finance ratios of a company from stock market
    Args:
        symbol: str (symbol of the company to get finance ratios)
        period: Literal['quarter', 'year'] = 'year' (period to get finance ratios)
    Returns:
        pd.DataFrame
    """
    finance = VCIFinance(symbol=symbol, period=period)
    return finance.ratio()


@with_output_format
def get_raw_report(symbol: str, period: Literal['quarter', 'year'] = 'year'):
    """
    Get raw report of a company from stock market
    Args:
        symbol: str (symbol of the company to get raw report)
        period: Literal['quarter', 'year'] = 'year' (period to get raw report)
    Returns:
        pd.DataFrame
    """
    finance = VCIFinance(symbol=symbol, period=period)
    return finance._get_report(mode='raw')


# Register all functions as MCP tools
finance_mcp.tool(get_income_statements)
finance_mcp.tool(get_balance_sheets)
finance_mcp.tool(get_cash_flows)
finance_mcp.tool(get_finance_ratios)
finance_mcp.tool(get_raw_report)
