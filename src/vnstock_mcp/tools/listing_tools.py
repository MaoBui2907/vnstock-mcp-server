from vnstock.explorer.vci.listing import Listing as VCIListing
import pandas as pd
from fastmcp import FastMCP
from vnstock_mcp.libs.utils import with_output_format

listing_mcp = FastMCP("Listing")


@with_output_format
def get_all_symbol_groups():
    """
    Get all symbol groups from stock market
    Returns:
        pd.DataFrame
    """
    df = pd.DataFrame([{
        'group': 'HOSE',
        'group_name': 'All symbols in HOSE'
    },
    {   
        'group': 'HNX',
        'group_name': 'All symbols in HNX'
    },
    {
        'group': 'UPCOM',
        'group_name': 'All symbols in UPCOM'
    },
    {
        'group': 'VN30',
        'group_name': 'All symbols in VN30'
    },
    {
        'group': 'VN100',
        'group_name': 'All symbols in VN100'
    },
    {
        'group': 'HNX30',
        'group_name': 'All symbols in HNX30'
    },
    {
        'group': 'VNMidCap',
        'group_name': 'All symbols in VNMidCap'
    },
    {
        'group': 'VNSmallCap',
        'group_name': 'All symbols in VNSmallCap'
    },
    {
        'group': 'VNAllShare',
        'group_name': 'All symbols in VNAllShare'
    },
    {
        'group': 'HNXCon',
        'group_name': 'All symbols in HNXCon'
    },
    {
        'group': 'HNXFin',
        'group_name': 'All symbols in HNXFin'
    },
    {
        'group': 'HNXLCap',
        'group_name': 'All symbols in HNXLCap'
    },
    {
        'group': 'HNXMSCap',
        'group_name': 'All symbols in HNXMSCap'
    },
    {
        'group': 'HNXMan',
        'group_name': 'All symbols in HNXMan'
    },
    {
        'group': 'ETF',
        'group_name': 'All symbols in ETF'
    },
    {
        'group': 'FU_INDEX',
        'group_name': 'All symbols in FU_INDEX'
    },
    {
        'group': 'CW',
        'group_name': 'All symbols in CW'
    }
    ])
    return df


@with_output_format
def get_all_industries():
    """
    Get all symbols from stock market
    Returns:
        pd.DataFrame or json
    """
    listing = VCIListing()
    return listing.industries_icb()


@with_output_format
def get_all_symbols_by_group(group: str):
    """
    Get all symbols from stock market
    Args:
        group: str (group name to get symbols)
    Returns:
        pd.DataFrame
    """
    listing = VCIListing()
    return listing.symbols_by_group(group=group)


@with_output_format
def get_all_symbols_by_industry(industry: str = None):
    """
    Get all symbols from stock market
    Args:
        industry: str = None (if None, return all symbols)
    Returns:
        pd.DataFrame or json
    """
    listing = VCIListing()
    df = listing.symbols_by_industries()
    if industry:
        codes = ['icb_code1', 'icb_code2', 'icb_code3', 'icb_code4']
        masks = []
        for col in codes:
            if col in df.columns:
                masks.append(df[col].astype(str) == industry)
        if masks:
            mask = masks[0]
            for m in masks[1:]:
                mask = mask | m
            df = df[mask]
    return df


@with_output_format
def get_all_symbols():
    """
    Get all symbols from stock market
    Returns:
        pd.DataFrame or json
    """
    listing = VCIListing()
    return listing.symbols_by_exchange()


@with_output_format
def get_all_symbols_detailed():
    """
    Get all symbols detailed from stock market
    Returns:
        pd.DataFrame
    """
    listing = VCIListing()
    return listing.symbols_by_exchange()


# Register all functions as MCP tools
listing_mcp.tool(get_all_symbol_groups)
listing_mcp.tool(get_all_industries)
listing_mcp.tool(get_all_symbols_by_group)
listing_mcp.tool(get_all_symbols_by_industry)
listing_mcp.tool(get_all_symbols)
listing_mcp.tool(get_all_symbols_detailed)
