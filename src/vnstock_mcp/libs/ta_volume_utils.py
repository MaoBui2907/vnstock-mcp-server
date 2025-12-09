"""
Volume Indicators for Technical Analysis.

This module contains volume-based technical indicators.
All functions take a DataFrame and return the DataFrame with indicator columns added.
"""

import pandas as pd
import pandas_ta as ta  # type: ignore

from .ta_core import _merge_indicator_result


def add_accumulation_distribution(data: pd.DataFrame) -> pd.DataFrame:
    """
    Add Accumulation/Distribution Line (A/D) to the data.

    Output columns: AD

    Args:
        data: pd.DataFrame (data to add accumulation distribution to)
    Returns:
        pd.DataFrame
    """
    result = data.ta.ad()
    return _merge_indicator_result(data, result)


def add_accumulation_distribution_oscillator(data: pd.DataFrame, fast_length: int = 3, slow_length: int = 10) -> pd.DataFrame:
    """
    Add Accumulation/Distribution Oscillator (ADOSC) to the data.

    Output columns: ADOSC

    Args:
        data: pd.DataFrame (data to add ADOSC to)
        fast_length: int (fast EMA length) Default: 3
        slow_length: int (slow EMA length) Default: 10
    Returns:
        pd.DataFrame
    """
    result = data.ta.adosc(fast=fast_length, slow=slow_length)
    return _merge_indicator_result(data, result)


def add_archer_on_balance_volume(
    data: pd.DataFrame,
    fast_length: int = 4,
    slow_length: int = 12,
    max_lookback: int = 2,
    min_lookback: int = 2,
) -> pd.DataFrame:
    """
    Add Archer On Balance Volume (AOBV) to the data.

    Output columns: OBV, OBV_min, OBV_max, OBVe_{fast}, OBVe_{slow}, AOBV_LR, AOBV_SR

    Args:
        data: pd.DataFrame (data to add AOBV to)
        fast_length: int (fast EMA length) Default: 4
        slow_length: int (slow EMA length) Default: 12
        max_lookback: int (lookback for max) Default: 2
        min_lookback: int (lookback for min) Default: 2
    Returns:
        pd.DataFrame
    """
    result = data.ta.aobv(fast=fast_length, slow=slow_length, max_lookback=max_lookback, min_lookback=min_lookback)
    return _merge_indicator_result(data, result)


def add_chaikin_money_flow(data: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    """
    Add Chaikin Money Flow (CMF) to the data.

    Output columns: CMF

    Args:
        data: pd.DataFrame (data to add CMF to)
        window: int (window size) Default: 20
    Returns:
        pd.DataFrame
    """
    result = data.ta.cmf(length=window)
    return _merge_indicator_result(data, result)


def add_elder_force_index(data: pd.DataFrame, window: int = 13) -> pd.DataFrame:
    """
    Add Elder Force Index (EFI) to the data.
    
    Output columns: EFI
    
    Args:
        data: pd.DataFrame (data to add EFI to)
        window: int (window size) Default: 13
    Returns:
        pd.DataFrame
    """
    result = data.ta.efi(length=window)
    return _merge_indicator_result(data, result)


def add_ease_of_movement(data: pd.DataFrame, window: int = 14, divisor: int = 100000000) -> pd.DataFrame:
    """
    Add Ease of Movement (EOM) to the data.
    
    Output columns: EOM
    
    Args:
        data: pd.DataFrame (data to add EOM to)
        window: int (window size) Default: 14
        divisor: int (divisor for EOM calculation) Default: 100000000
    Returns:
        pd.DataFrame
    """
    result = data.ta.eom(length=window, divisor=divisor)
    return _merge_indicator_result(data, result)


def add_klinger_volume_oscillator(data: pd.DataFrame, fast_length: int = 34, slow_length: int = 55, signal_length: int = 13) -> pd.DataFrame:
    """
    Add Klinger Volume Oscillator (KVO) to the data.
    
    Output columns: KVO, KVOs (Signal)
    
    Args:
        data: pd.DataFrame (data to add KVO to)
        fast_length: int (fast EMA length) Default: 34
        slow_length: int (slow EMA length) Default: 55
        signal_length: int (signal EMA length) Default: 13
    Returns:
        pd.DataFrame
    """
    result = data.ta.kvo(fast=fast_length, slow=slow_length, signal=signal_length)
    return _merge_indicator_result(data, result)


def add_money_flow_index(data: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    """
    Add Money Flow Index (MFI) to the data.
    
    Output columns: MFI
    
    Args:
        data: pd.DataFrame (data to add MFI to)
        window: int (window size) Default: 14
    Returns:
        pd.DataFrame
    """
    result = data.ta.mfi(length=window)
    return _merge_indicator_result(data, result)


def add_negative_volume_index(data: pd.DataFrame) -> pd.DataFrame:
    """
    Add Negative Volume Index (NVI) to the data.
    
    Output columns: NVI
    
    Args:
        data: pd.DataFrame (data to add NVI to)
    Returns:
        pd.DataFrame
    """
    result = data.ta.nvi()
    return _merge_indicator_result(data, result)


def add_on_balance_volume(data: pd.DataFrame) -> pd.DataFrame:
    """
    Add On Balance Volume (OBV) to the data.
    
    Output columns: OBV
    
    Args:
        data: pd.DataFrame (data to add OBV to)
    Returns:
        pd.DataFrame
    """
    result = data.ta.obv()
    return _merge_indicator_result(data, result)


# Note: PVI (Positive Volume Index) is commented out because it returns empty results
# def add_positive_volume_index(data: pd.DataFrame) -> pd.DataFrame:
#     """
#     Add Positive Volume Index (PVI) to the data.
#     
#     Output columns: PVI
#     
#     Args:
#         data: pd.DataFrame (data to add PVI to)
#     Returns:
#         pd.DataFrame
#     """
#     result = data.ta.pvi()
#     return _merge_indicator_result(data, result)


def add_percentage_volume_oscillator(data: pd.DataFrame, fast_length: int = 12, slow_length: int = 26, signal_length: int = 9) -> pd.DataFrame:
    """
    Add Percentage Volume Oscillator (PVO) to the data.
    
    Output columns: PVO, PVOh (Histogram), PVOs (Signal)
    
    Args:
        data: pd.DataFrame (data to add PVO to)
        fast_length: int (fast EMA length) Default: 12
        slow_length: int (slow EMA length) Default: 26
        signal_length: int (signal EMA length) Default: 9
    Returns:
        pd.DataFrame
    """
    result = data.ta.pvo(fast=fast_length, slow=slow_length, signal=signal_length)
    return _merge_indicator_result(data, result)


def add_price_volume(data: pd.DataFrame) -> pd.DataFrame:
    """
    Add Price Volume (PVOL) to the data.
    
    Output columns: PVOL
    
    Args:
        data: pd.DataFrame (data to add PVOL to)
    Returns:
        pd.DataFrame
    """
    result = data.ta.pvol()
    return _merge_indicator_result(data, result)


def add_price_volume_rank(data: pd.DataFrame) -> pd.DataFrame:
    """
    Add Price Volume Rank (PVR) to the data.
    
    Output columns: PVR
    
    Args:
        data: pd.DataFrame (data to add PVR to)
    Returns:
        pd.DataFrame
    """
    result = data.ta.pvr()
    return _merge_indicator_result(data, result)


def add_price_volume_trend(data: pd.DataFrame) -> pd.DataFrame:
    """
    Add Price Volume Trend (PVT) to the data.
    
    Output columns: PVT
    
    Args:
        data: pd.DataFrame (data to add PVT to)
    Returns:
        pd.DataFrame
    """
    result = data.ta.pvt()
    return _merge_indicator_result(data, result)


def add_time_segmented_volume(data: pd.DataFrame, window: int = 18, signal_length: int = 10) -> pd.DataFrame:
    """
    Add Time Segmented Volume (TSV) to the data.
    
    Output columns: TSV, TSVs (Signal), TSVr (Ratio)
    
    Args:
        data: pd.DataFrame (data to add TSV to)
        window: int (window size) Default: 18
        signal_length: int (signal length) Default: 10
    Returns:
        pd.DataFrame
    """
    result = data.ta.tsv(length=window, signal=signal_length)
    return _merge_indicator_result(data, result)


def add_volume_weighted_moving_average(data: pd.DataFrame, window: int = 10) -> pd.DataFrame:
    """
    Add Volume Weighted Moving Average (VWMA) to the data.
    
    Output columns: VWMA
    
    Args:
        data: pd.DataFrame (data to add VWMA to)
        window: int (window size) Default: 10
    Returns:
        pd.DataFrame
    """
    result = data.ta.vwma(length=window)
    return _merge_indicator_result(data, result)


# Note: The following indicators are commented out because they have issues in pandas_ta:
#
# - add_positive_volume_index (pvi): Returns empty results
# - add_volume_heatmap (vhm): Returns original DataFrame instead of indicator values
# - add_volume_profile (vp): Not available in pandas_ta
# - add_volume_weighted_average_price (vwap): Requires DatetimeIndex, complex setup


# Volume Indicator Registry
VOLUME_INDICATOR_REGISTRY: dict = {
    "ad": add_accumulation_distribution,
    "accumulation_distribution": add_accumulation_distribution,
    "adosc": add_accumulation_distribution_oscillator,
    "accumulation_distribution_oscillator": add_accumulation_distribution_oscillator,
    "aobv": add_archer_on_balance_volume,
    "archer_on_balance_volume": add_archer_on_balance_volume,
    "cmf": add_chaikin_money_flow,
    "chaikin_money_flow": add_chaikin_money_flow,
    "efi": add_elder_force_index,
    "elder_force_index": add_elder_force_index,
    "eom": add_ease_of_movement,
    "ease_of_movement": add_ease_of_movement,
    "kvo": add_klinger_volume_oscillator,
    "klinger_volume_oscillator": add_klinger_volume_oscillator,
    "mfi": add_money_flow_index,
    "money_flow_index": add_money_flow_index,
    "nvi": add_negative_volume_index,
    "negative_volume_index": add_negative_volume_index,
    "obv": add_on_balance_volume,
    "on_balance_volume": add_on_balance_volume,
    "pvo": add_percentage_volume_oscillator,
    "percentage_volume_oscillator": add_percentage_volume_oscillator,
    "pvol": add_price_volume,
    "price_volume": add_price_volume,
    "pvr": add_price_volume_rank,
    "price_volume_rank": add_price_volume_rank,
    "pvt": add_price_volume_trend,
    "price_volume_trend": add_price_volume_trend,
    "tsv": add_time_segmented_volume,
    "time_segmented_volume": add_time_segmented_volume,
    "vwma": add_volume_weighted_moving_average,
    "volume_weighted_moving_average": add_volume_weighted_moving_average,
}
