from vnstock.explorer import vci
from vnstock.explorer.vci.const import _GROUP_CODE
import pandas as pd

def get_all_symbols_with_groups():
    group_df = pd.DataFrame()
    vci_listing = vci.listing.Listing()
    for group in _GROUP_CODE:
        try:
            symbols = vci_listing.symbols_by_group(group=group)
        except Exception as e:
            continue
        df = pd.DataFrame({'symbol': symbols})
        df['group'] = group
        group_df = pd.concat([group_df, df])

    group_df = group_df[['symbol', 'group']]
    return group_df