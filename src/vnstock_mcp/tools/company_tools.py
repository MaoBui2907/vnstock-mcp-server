from vnstock.explorer.tcbs.company import Company as TCBSCompany
from vnstock.explorer.vci.company import Company as VCICompany
from vnstock.explorer.vci.listing import Listing as VCIListing
from typing import Literal
from fastmcp import FastMCP
from vnstock_mcp.libs.utils import with_output_format
from vnstock_mcp.libs.vnstock_utils import get_all_symbols_with_groups

company_mcp = FastMCP("Company")


@with_output_format
def list_all_icb_industries():
    """
    List all ICB industries from stock market
    Returns:
        pd.DataFrame
    """
    icb_industries = VCIListing().industries_icb()
    icb_industries['icb_code'] = icb_industries['icb_code'].astype(str)
    icb_industries['vi_icb_name'] = icb_industries['icb_name'].astype(str)
    icb_industries['en_icb_name'] = icb_industries['en_icb_name'].astype(str)
    icb_industries['level'] = icb_industries['level'].astype(int)
    icb_industries = icb_industries[['icb_code', 'vi_icb_name', 'en_icb_name', 'level']]
    return icb_industries


@with_output_format
def list_all_companies_with_details():
    """
    List all companies from stock market with details
    Returns:
        pd.DataFrame
    """
    symbols_with_groups = get_all_symbols_with_groups()
    symbols_by_industries = VCIListing().symbols_by_industries()
    symbols_by_exchange = VCIListing().symbols_by_exchange()

    final_df = symbols_by_exchange.copy()
    final_df['group'] = final_df['symbol'].apply(lambda sym: symbols_with_groups[symbols_with_groups['symbol'] == sym]['group'].tolist())
    final_df['icb_code1'] = final_df['symbol'].apply(lambda sym: symbols_by_industries[symbols_by_industries['symbol'] == sym]['icb_code1'].tolist()[0] if len(symbols_by_industries[symbols_by_industries['symbol'] == sym]['icb_code1'].tolist()) > 0 else "")
    final_df['icb_code2'] = final_df['symbol'].apply(lambda sym: symbols_by_industries[symbols_by_industries['symbol'] == sym]['icb_code2'].tolist()[0] if len(symbols_by_industries[symbols_by_industries['symbol'] == sym]['icb_code2'].tolist()) > 0 else "")
    final_df['icb_code3'] = final_df['symbol'].apply(lambda sym: symbols_by_industries[symbols_by_industries['symbol'] == sym]['icb_code3'].tolist()[0] if len(symbols_by_industries[symbols_by_industries['symbol'] == sym]['icb_code3'].tolist()) > 0 else "")
    final_df['icb_code4'] = final_df['symbol'].apply(lambda sym: symbols_by_industries[symbols_by_industries['symbol'] == sym]['icb_code4'].tolist()[0] if len(symbols_by_industries[symbols_by_industries['symbol'] == sym]['icb_code4'].tolist()) > 0 else "")

    final_df['company_name'] = final_df['organ_name'].fillna("Unknown")
    final_df = final_df[['symbol', 'company_name', 'icb_code1', 'icb_code2', 'icb_code3', 'icb_code4', 'group', 'exchange']]
    return final_df


@with_output_format
def get_company_overview(symbol: str):
    """
    Get company overview from stock market
    Args:
        symbol: str
    Returns:
        pd.DataFrame
    """
    equity = TCBSCompany(symbol=symbol)
    return equity.overview()


@with_output_format
def get_company_news(symbol: str, page_size: int = 10, page: int = 0):
    """
    Get company news from stock market
    Args:
        symbol: str
        page_size: int = 10
        page: int = 0
    Returns:
        pd.DataFrame
    """
    equity = TCBSCompany(symbol=symbol)
    return equity.news(page_size=page_size, page=page)


@with_output_format
def get_company_events(symbol: str, page_size: int = 10, page: int = 0):
    """
    Get company events from stock market
    Args:
        symbol: str
        page_size: int = 10
        page: int = 0
    Returns:
        pd.DataFrame
    """
    equity = TCBSCompany(symbol=symbol)
    return equity.events(page_size=page_size, page=page)


@with_output_format
def get_company_shareholders(symbol: str):
    """
    Get company shareholders from stock market
    Args:
        symbol: str
    Returns:
        pd.DataFrame
    """
    equity = TCBSCompany(symbol=symbol)
    return equity.shareholders()


@with_output_format
def get_company_officers(symbol: str, filter_by: Literal['working', "all", 'resigned'] = 'working'):
    """
    Get company officers from stock market
    Args:
        symbol: str
        filter_by: Literal['working', "all", 'resigned'] = 'working'
    Returns:
        pd.DataFrame
    """
    equity = TCBSCompany(symbol=symbol)
    return equity.officers(filter_by=filter_by)


@with_output_format
def get_company_subsidiaries(symbol: str, filter_by: Literal["all", "subsidiary"] = "all"):
    """
    Get company subsidiaries from stock market
    Args:
        symbol: str
        filter_by: Literal["all", "subsidiary"] = "all"
    Returns:
        pd.DataFrame
    """
    equity = TCBSCompany(symbol=symbol)
    return equity.subsidiaries(filter_by=filter_by)


@with_output_format
def get_company_reports(symbol: str):
    """
    Get company reports from stock market
    Args:
        symbol: str
    Returns:
        pd.DataFrame
    """
    equity = VCICompany(symbol=symbol)
    return equity.reports()


@with_output_format
def get_company_dividends(symbol: str):
    """
    Get company dividends from stock market
    Args:
        symbol: str
    Returns:
        pd.DataFrame
    """
    equity = TCBSCompany(symbol=symbol)
    return equity.dividends()


@with_output_format
def get_company_insider_deals(symbol: str):
    """
    Get company insider deals from stock market
    Args:
        symbol: str
    Returns:
        pd.DataFrame
    """
    equity = TCBSCompany(symbol=symbol)
    return equity.insider_deals()


@with_output_format
def get_company_ratio_summary(symbol: str):
    """
    Get company ratio summary from stock market
    Args:
        symbol: str
    Returns:
        pd.DataFrame
    """
    equity = VCICompany(symbol=symbol)
    return equity.ratio_summary()


@with_output_format
def get_company_trading_stats(symbol: str):
    """
    Get company trading stats from stock market
    Args:
        symbol: str
    Returns:
        pd.DataFrame
    """
    equity = VCICompany(symbol=symbol)
    return equity.trading_stats()


# Register all functions as MCP tools
company_mcp.tool(list_all_icb_industries)
company_mcp.tool(list_all_companies_with_details)
company_mcp.tool(get_company_overview)
company_mcp.tool(get_company_news)
company_mcp.tool(get_company_events)
company_mcp.tool(get_company_shareholders)
company_mcp.tool(get_company_officers)
company_mcp.tool(get_company_subsidiaries)
company_mcp.tool(get_company_reports)
company_mcp.tool(get_company_dividends)
company_mcp.tool(get_company_insider_deals)
company_mcp.tool(get_company_ratio_summary)
company_mcp.tool(get_company_trading_stats)
