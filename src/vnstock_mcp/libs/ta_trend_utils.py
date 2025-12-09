"""
Trend Indicators for Technical Analysis.

This module contains trend-based technical indicators.
All functions take a DataFrame and return the DataFrame with indicator columns added.
"""
import pandas as pd
import pandas_ta as ta  # type: ignore

from .ta_core import _merge_indicator_result


def add_average_directional_movement(data: pd.DataFrame, window: int = 14, signal_length: int = 14, adx_length: int = 2, scalar: float = 100) -> pd.DataFrame:
    """
    Add Average Directional Movement Index (ADX) to the data.
    
    Output columns: ADX, ADXR, DMP, DMN
    
    Args:
        data: pd.DataFrame (data to add ADX to)
        window: int (window size for ADX) Default: 14
        signal_length: int (length for signal) Default: 14
        adx_length: int (length for ADXR) Default: 2
        scalar: float (scalar for ADX) Default: 100
    Returns:
        pd.DataFrame
    """
    result = data.ta.adx(length=window, signal=signal_length, adx_length=adx_length, scalar=scalar)
    return _merge_indicator_result(data, result)


def add_alpha_trend(data: pd.DataFrame, window: int = 14, multiplier: float = 1, atr_period: int = 50) -> pd.DataFrame:
    """
    Add Alpha Trend indicator to the data.
    
    Output columns: ALPHAT (Alpha Trend), ALPHATl (Alpha Trend Long)
    
    Args:
        data: pd.DataFrame (data to add alpha trend to)
        window: int (window size for alpha trend) Default: 14
        multiplier: float (multiplier for ATR) Default: 1
        atr_period: int (period for ATR) Default: 50
    Returns:
        pd.DataFrame
    """
    result = data.ta.alphatrend(length=window, multiplier=multiplier, atr_period=atr_period)
    return _merge_indicator_result(data, result)


def add_archer_moving_average_trend(data: pd.DataFrame, fast_length: int = 8, slow_length: int = 21, lookback_length: int = 2) -> pd.DataFrame:
    """
    Add Archer Moving Average Trend (AMAT) to the data.
    
    Output columns: AMATe_LR (Long Run), AMATe_SR (Short Run)
    
    Args:
        data: pd.DataFrame (data to add AMAT to)
        fast_length: int (fast length for AMAT) Default: 8
        slow_length: int (slow length for AMAT) Default: 21
        lookback_length: int (lookback length for AMAT) Default: 2
    Returns:
        pd.DataFrame
    """
    result = data.ta.amat(fast=fast_length, slow=slow_length, lookback=lookback_length)
    return _merge_indicator_result(data, result)


def add_aroon_and_aroon_oscillator(data: pd.DataFrame, window: int = 14, scalar: float = 100) -> pd.DataFrame:
    """
    Add Aroon indicator and Aroon Oscillator to the data.
    
    Output columns: AROOND (Aroon Down), AROONU (Aroon Up), AROONOSC (Aroon Oscillator)
    
    Args:
        data: pd.DataFrame (data to add Aroon to)
        window: int (window size for Aroon) Default: 14
        scalar: float (scalar for Aroon) Default: 100
    Returns:
        pd.DataFrame
    """
    result = data.ta.aroon(length=window, scalar=scalar)
    return _merge_indicator_result(data, result)


def add_choppiness_index(data: pd.DataFrame, window: int = 14, atr_length: int = 1, scalar: float = 100) -> pd.DataFrame:
    """
    Add Choppiness Index (CHOP) to the data.
    
    Output columns: CHOP
    
    Args:
        data: pd.DataFrame (data to add CHOP to)
        window: int (window size for CHOP) Default: 14
        atr_length: int (length for ATR) Default: 1
        scalar: float (scalar for CHOP) Default: 100
    Returns:
        pd.DataFrame
    """
    result = data.ta.chop(length=window, atr_length=atr_length, scalar=scalar)
    return _merge_indicator_result(data, result)


def add_chande_kroll_stop(data: pd.DataFrame, p: int = 10, x: float = 3, q: int = 20) -> pd.DataFrame:
    """
    Add Chande Kroll Stop to the data.
    
    Output columns: CKSPl (Long Stop), CKSPs (Short Stop)
    
    Args:
        data: pd.DataFrame (data to add Chande Kroll Stop to)
        p: int (first period) Default: 10
        x: float (multiplier) Default: 3
        q: int (second period) Default: 20
    Returns:
        pd.DataFrame
    """
    result = data.ta.cksp(p=p, x=x, q=q)
    return _merge_indicator_result(data, result)


def add_decay(data: pd.DataFrame, window: int = 1) -> pd.DataFrame:
    """
    Add Linear Decay indicator to the data.
    
    Output columns: LDECAY
    
    Args:
        data: pd.DataFrame (data to add decay to)
        window: int (window size for decay) Default: 1
    Returns:
        pd.DataFrame
    """
    result = data.ta.decay(length=window)
    return _merge_indicator_result(data, result)


def add_decreasing(data: pd.DataFrame, window: int = 1) -> pd.DataFrame:
    """
    Add Decreasing indicator to the data. Returns 1 if price is decreasing, 0 otherwise.
    
    Output columns: DEC
    
    Args:
        data: pd.DataFrame (data to add decreasing to)
        window: int (window size for decreasing) Default: 1
    Returns:
        pd.DataFrame
    """
    result = data.ta.decreasing(length=window)
    return _merge_indicator_result(data, result)


def add_detrend_price_oscillator(data: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    """
    Add Detrend Price Oscillator (DPO) to the data.
    
    Output columns: DPO
    
    Args:
        data: pd.DataFrame (data to add DPO to)
        window: int (window size for DPO) Default: 20
    Returns:
        pd.DataFrame
    """
    result = data.ta.dpo(length=window)
    return _merge_indicator_result(data, result)


def add_hilbert_transform_trendline(data: pd.DataFrame) -> pd.DataFrame:
    """
    Add Hilbert Transform Trendline to the data.
    
    Output columns: HT_TL
    
    Args:
        data: pd.DataFrame (data to add Hilbert Transform Trendline to)
    Returns:
        pd.DataFrame
    """
    result = data.ta.ht_trendline()
    return _merge_indicator_result(data, result)


def add_increasing(data: pd.DataFrame, window: int = 1) -> pd.DataFrame:
    """
    Add Increasing indicator to the data. Returns 1 if price is increasing, 0 otherwise.
    
    Output columns: INC
    
    Args:
        data: pd.DataFrame (data to add increasing to)
        window: int (window size for increasing) Default: 1
    Returns:
        pd.DataFrame
    """
    result = data.ta.increasing(length=window)
    return _merge_indicator_result(data, result)


def add_parabolic_stop_and_reverse(data: pd.DataFrame, af0: float = 0.02, af: float = 0.02, af_max: float = 0.2) -> pd.DataFrame:
    """
    Add Parabolic Stop and Reverse (PSAR) to the data.
    
    Output columns: PSARl (Long), PSARs (Short), PSARaf (Acceleration Factor), PSARr (Reversal)
    
    Args:
        data: pd.DataFrame (data to add PSAR to)
        af0: float (acceleration factor start) Default: 0.02
        af: float (acceleration factor) Default: 0.02
        af_max: float (acceleration factor max) Default: 0.2
    Returns:
        pd.DataFrame
    """
    result = data.ta.psar(af0=af0, af=af, af_max=af_max)
    return _merge_indicator_result(data, result)


def add_q_stick(data: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    """
    Add Q Stick indicator to the data.
    
    Output columns: QS
    
    Args:
        data: pd.DataFrame (data to add Q Stick to)
        window: int (window size for Q Stick) Default: 14
    Returns:
        pd.DataFrame
    """
    result = data.ta.qstick(length=window)
    return _merge_indicator_result(data, result)


def add_random_walk_index(data: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    """
    Add Random Walk Index (RWI) to the data.
    
    Output columns: RWIh (High), RWIl (Low)
    
    Args:
        data: pd.DataFrame (data to add RWI to)
        window: int (window size for RWI) Default: 14
    Returns:
        pd.DataFrame
    """
    result = data.ta.rwi(length=window)
    return _merge_indicator_result(data, result)


def add_trend_flex(data: pd.DataFrame, window: int = 20, smooth_length: int = 20, reflex_period: float = 0.04) -> pd.DataFrame:
    """
    Add Trend Flex indicator to the data.
    
    Output columns: TRENDFLEX
    
    Args:
        data: pd.DataFrame (data to add Trend Flex to)
        window: int (window size for Trend Flex) Default: 20
        smooth_length: int (smooth length for Trend Flex) Default: 20
        reflex_period: float (reflex period) Default: 0.04
    Returns:
        pd.DataFrame
    """
    result = data.ta.trendflex(length=window, smooth=smooth_length, reflex_period=reflex_period)
    return _merge_indicator_result(data, result)


def add_vertical_horizontal_filter(data: pd.DataFrame, window: int = 28) -> pd.DataFrame:
    """
    Add Vertical Horizontal Filter (VHF) to the data.
    
    Output columns: VHF
    
    Args:
        data: pd.DataFrame (data to add VHF to)
        window: int (window size for VHF) Default: 28
    Returns:
        pd.DataFrame
    """
    result = data.ta.vhf(length=window)
    return _merge_indicator_result(data, result)


def add_vortex_indicator(data: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    """
    Add Vortex Indicator to the data.
    
    Output columns: VTXP (Positive), VTXM (Negative)
    
    Args:
        data: pd.DataFrame (data to add Vortex Indicator to)
        window: int (window size for Vortex) Default: 14
    Returns:
        pd.DataFrame
    """
    result = data.ta.vortex(length=window)
    return _merge_indicator_result(data, result)


def add_zig_zag(data: pd.DataFrame, deviation: float = 5.0, min_bars: int = 10) -> pd.DataFrame:
    """
    Add Zig Zag indicator to the data.
    
    Output columns: ZIGZAGs_{deviation}%_{min_bars} (Support), ZIGZAGv_{deviation}%_{min_bars} (Value), ZIGZAGd_{deviation}%_{min_bars} (Direction)
    
    Note: Column names include parameters, e.g., ZIGZAGs_5.0%_10, ZIGZAGv_5.0%_10, ZIGZAGd_5.0%_10
    
    Args:
        data: pd.DataFrame (data to add Zig Zag to)
        deviation: float (percentage deviation for reversal) Default: 5.0
        min_bars: int (minimum bars between pivots) Default: 10
    Returns:
        pd.DataFrame
    """
    result = data.ta.zigzag(deviation=deviation, min_bars=min_bars)
    return _merge_indicator_result(data, result)


# Note: The following indicators are commented out because they are not available
# or have issues in pandas_ta:
#
# - add_short_run: Returns original DataFrame instead of indicator values
# - add_ttm_trend: Not available in pandas_ta
# - add_long_run: Not available in pandas_ta


# Trend Indicator Registry
TREND_INDICATOR_REGISTRY: dict = {
    "adx": add_average_directional_movement,
    "average_directional_movement": add_average_directional_movement,
    "alphatrend": add_alpha_trend,
    "alpha_trend": add_alpha_trend,
    "amat": add_archer_moving_average_trend,
    "archer_moving_average_trend": add_archer_moving_average_trend,
    "aroon": add_aroon_and_aroon_oscillator,
    "aroon_oscillator": add_aroon_and_aroon_oscillator,
    "chop": add_choppiness_index,
    "choppiness_index": add_choppiness_index,
    "cksp": add_chande_kroll_stop,
    "chande_kroll_stop": add_chande_kroll_stop,
    "decay": add_decay,
    "decreasing": add_decreasing,
    "dpo": add_detrend_price_oscillator,
    "detrend_price_oscillator": add_detrend_price_oscillator,
    "ht_trendline": add_hilbert_transform_trendline,
    "hilbert_transform_trendline": add_hilbert_transform_trendline,
    "increasing": add_increasing,
    "psar": add_parabolic_stop_and_reverse,
    "parabolic_stop_and_reverse": add_parabolic_stop_and_reverse,
    "qstick": add_q_stick,
    "q_stick": add_q_stick,
    "rwi": add_random_walk_index,
    "random_walk_index": add_random_walk_index,
    "trendflex": add_trend_flex,
    "trend_flex": add_trend_flex,
    "vhf": add_vertical_horizontal_filter,
    "vertical_horizontal_filter": add_vertical_horizontal_filter,
    "vortex": add_vortex_indicator,
    "vortex_indicator": add_vortex_indicator,
    "zigzag": add_zig_zag,
    "zig_zag": add_zig_zag,
}
