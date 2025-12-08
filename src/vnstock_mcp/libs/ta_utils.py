import pandas as pd
import pandas_ta as ta # type: ignore
import re
import inspect
from typing import Any


def _strip_numeric_suffix(col_name: str) -> str:
    """
    Remove numeric suffix from column name.
    Examples:
        'MACD_12_26_9' -> 'MACD'
        'MACDh_12_26_9' -> 'MACDh'
        'STOCHk_14_3_3' -> 'STOCHk'
        'SQZ_ON' -> 'SQZ_ON' (no numeric suffix)
    """
    # Match pattern: name followed by underscore and numbers (with possible dots)
    # Keep the base name part
    match = re.match(r'^([A-Za-z_]+?)(?:_[\d._]+)?$', col_name)
    if match:
        return match.group(1).rstrip('_')
    return col_name


def _merge_indicator_result(data: pd.DataFrame, result, rename_map: dict = None, fillna_value: float = 0) -> pd.DataFrame:
    """
    Merge indicator result into data DataFrame.
    
    Args:
        data: Original DataFrame
        result: Result from pandas_ta (Series or DataFrame)
        rename_map: Optional dict to rename columns {old_name_pattern: new_name}
        fillna_value: Value to fill NaN with (default: 0)
    
    Returns:
        DataFrame with indicator columns added (NaN values filled with fillna_value)
    """
    if result is None:
        return data
    
    if isinstance(result, pd.Series):
        # Single column result
        name = _strip_numeric_suffix(result.name) if result.name else 'indicator'
        data[name] = result.fillna(fillna_value)
    elif isinstance(result, pd.DataFrame):
        # Multi-column result
        for col in result.columns:
            new_name = _strip_numeric_suffix(col)
            if rename_map and col in rename_map:
                new_name = rename_map[col]
            data[new_name] = result[col].fillna(fillna_value)
    
    return data


# MOMENTUM INDICATORS
def add_awesome_oscillator(data: pd.DataFrame, fast_length: int = 5, slow_length: int = 34) -> pd.DataFrame:
    """
    Add awesome oscillator to the data.
    
    Output columns: AO
    
    Args:
        data: pd.DataFrame (data to add awesome oscillator to)
        fast_length: int (fast length for awesome oscillator) Default: 5
        slow_length: int (slow length for awesome oscillator) Default: 34
    Returns:
        pd.DataFrame
    """
    result = data.ta.ao(fast=fast_length, slow=slow_length)
    return _merge_indicator_result(data, result)


def add_absolute_price_oscillator(data: pd.DataFrame, fast_length: int = 12, slow_length: int = 26) -> pd.DataFrame:
    """
    Add absolute price oscillator to the data.
    
    Output columns: APO
    
    Args:
        data: pd.DataFrame (data to add absolute price oscillator to)
        fast_length: int (fast length for absolute price oscillator) Default: 12    
        slow_length: int (slow length for absolute price oscillator) Default: 26
    Returns:
        pd.DataFrame
    """
    result = data.ta.apo(fast=fast_length, slow=slow_length)
    return _merge_indicator_result(data, result)


def add_bias(data: pd.DataFrame, window: int = 26) -> pd.DataFrame:
    """
    Add bias to the data.
    
    Output columns: BIAS
    
    Args:
        data: pd.DataFrame (data to add bias to)
        window: int (window size for bias) Default: 26
    Returns:
        pd.DataFrame
    """
    result = data.ta.bias(length=window)
    return _merge_indicator_result(data, result)


def add_balance_of_power(data: pd.DataFrame, scalar: float = 1) -> pd.DataFrame:
    """
    Add balance of power to the data.
    
    Output columns: BOP
    
    Args:
        data: pd.DataFrame (data to add balance of power to)
        scalar: float (scalar for balance of power) Default: 1
    Returns:
        pd.DataFrame
    """
    result = data.ta.bop(scalar=scalar)
    return _merge_indicator_result(data, result)


def add_br_and_ar(data: pd.DataFrame, window: int = 26, scalar: float = 100) -> pd.DataFrame:
    """
    Add BR and AR indicators to the data.
    
    Output columns: AR, BR
    
    Args:
        data: pd.DataFrame (data to add br and ar to)
        window: int (window size for br and ar) Default: 26
        scalar: float (scalar for br and ar) Default: 100
    Returns:
        pd.DataFrame
    """
    result = data.ta.brar(length=window, scalar=scalar)
    return _merge_indicator_result(data, result)


def add_commodity_channel_index(data: pd.DataFrame, window: int = 14, scalar: float = 0.015) -> pd.DataFrame:
    """
    Add commodity channel index to the data.
    
    Output columns: CCI
    
    Args:
        data: pd.DataFrame (data to add commodity channel index to)
        window: int (window size for commodity channel index) Default: 14
        scalar: float (scalar for commodity channel index) Default: 0.015
    Returns:
        pd.DataFrame
    """
    result = data.ta.cci(length=window, scalar=scalar)
    return _merge_indicator_result(data, result)


def add_chande_forecast_oscillator(data: pd.DataFrame, window: int = 9, scalar: float = 100) -> pd.DataFrame:
    """
    Add chande forecast oscillator to the data.
    
    Output columns: CFO
    
    Args:
        data: pd.DataFrame (data to add chande forecast oscillator to)
        window: int (window size for chande forecast oscillator) Default: 9
        scalar: float (scalar for chande forecast oscillator) Default: 100
    Returns:
        pd.DataFrame
    """
    result = data.ta.cfo(length=window, scalar=scalar)
    return _merge_indicator_result(data, result)


def add_center_of_gravity(data: pd.DataFrame, window: int = 10) -> pd.DataFrame:
    """
    Add center of gravity to the data.
    
    Output columns: CG
    
    Args:
        data: pd.DataFrame (data to add center of gravity to)
        window: int (window size for center of gravity) Default: 10
    Returns:
        pd.DataFrame
    """
    result = data.ta.cg(length=window)
    return _merge_indicator_result(data, result)


def add_chande_momentum_oscillator(data: pd.DataFrame, window: int = 10, scalar: float = 100) -> pd.DataFrame:
    """
    Add chande momentum oscillator to the data.
    
    Output columns: CMO
    
    Args:
        data: pd.DataFrame (data to add chande momentum oscillator to)
        window: int (window size for chande momentum oscillator) Default: 10
        scalar: float (scalar for chande momentum oscillator) Default: 100
    Returns:
        pd.DataFrame
    """
    result = data.ta.cmo(length=window, scalar=scalar)
    return _merge_indicator_result(data, result)


def add_coppock_curve(data: pd.DataFrame, window: int = 10, fast_length: int = 11, slow_length: int = 14) -> pd.DataFrame:
    """
    Add coppock curve to the data.
    
    Output columns: COPPOCK
    
    Args:
        data: pd.DataFrame (data to add coppock curve to)
        window: int (window size for coppock curve) Default: 10
        fast_length: int (fast length for coppock curve) Default: 11
        slow_length: int (slow length for coppock curve) Default: 14
    Returns:
        pd.DataFrame
    """
    result = data.ta.coppock(length=window, fast=fast_length, slow=slow_length)
    return _merge_indicator_result(data, result)


def add_connors_relative_strength_index(data: pd.DataFrame, rsi_window: int = 3, streak_length: int = 2, rank_length: int = 100, scalar: float = 100) -> pd.DataFrame:
    """
    Add connors relative strength index to the data.
    
    Output columns: CRSI
    
    Args:
        data: pd.DataFrame (data to add connors relative strength index to)
        rsi_window: int (window size for rsi) Default: 3
        streak_length: int (window size for streak) Default: 2
        rank_length: int (window size for rank) Default: 100
        scalar: float (scalar for connors relative strength index) Default: 100
    Returns:
        pd.DataFrame
    """
    result = data.ta.crsi(rsi_length=rsi_window, streak_length=streak_length, rank_length=rank_length, scalar=scalar)
    return _merge_indicator_result(data, result)


def add_correlation_trend_indicator(data: pd.DataFrame, window: int = 12) -> pd.DataFrame:
    """
    Add correlation trend indicator to the data.
    
    Output columns: CTI
    
    Args:
        data: pd.DataFrame (data to add correlation trend indicator to)
        window: int (window size for correlation trend indicator) Default: 12
    Returns:
        pd.DataFrame
    """
    result = data.ta.cti(length=window)
    return _merge_indicator_result(data, result)


def add_directional_movement(data: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    """
    Add directional movement to the data.
    
    Output columns: DMP (Plus Directional Movement), DMN (Minus Directional Movement)
    
    Args:
        data: pd.DataFrame (data to add directional movement to)
        window: int (window size for directional movement) Default: 14
    Returns:
        pd.DataFrame
    """
    result = data.ta.dm(length=window)
    return _merge_indicator_result(data, result)


def add_efficiency_ratio(data: pd.DataFrame, window: int = 10) -> pd.DataFrame:
    """
    Add efficiency ratio to the data.
    
    Output columns: ER
    
    Args:
        data: pd.DataFrame (data to add efficiency ratio to)
        window: int (window size for efficiency ratio) Default: 10
    Returns:
        pd.DataFrame
    """
    result = data.ta.er(length=window)
    return _merge_indicator_result(data, result)


def add_elder_ray_index(data: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    """
    Add elder ray index to the data.
    
    Output columns: BULLP (Bull Power), BEARP (Bear Power)
    
    Args:
        data: pd.DataFrame (data to add elder ray index to)
        window: int (window size for elder ray index) Default: 14
    Returns:
        pd.DataFrame
    """
    result = data.ta.eri(length=window)
    return _merge_indicator_result(data, result)


def add_fisher_transform(data: pd.DataFrame, window: int = 9) -> pd.DataFrame:
    """
    Add fisher transform to the data.
    
    Output columns: FISHERT (Fisher Transform), FISHERTs (Signal)
    
    Args:
        data: pd.DataFrame (data to add fisher transform to)
        window: int (window size for fisher transform) Default: 9
    Returns:
        pd.DataFrame
    """
    result = data.ta.fisher(length=window)
    return _merge_indicator_result(data, result)


def add_inertia(data: pd.DataFrame, window: int = 20, rvi_length: int = 14) -> pd.DataFrame:
    """
    Add inertia to the data.
    
    Output columns: INERTIA
    
    Args:
        data: pd.DataFrame (data to add inertia to)
        window: int (window size for inertia) Default: 20
        rvi_length: int (window size for rvi) Default: 14
    Returns:
        pd.DataFrame
    """
    result = data.ta.inertia(length=window, rvi_length=rvi_length)
    return _merge_indicator_result(data, result)


def add_kdj(data: pd.DataFrame, window: int = 9, signal_window: int = 3) -> pd.DataFrame:
    """
    Add KDJ indicator to the data.
    
    Output columns: K, D, J
    
    Args:
        data: pd.DataFrame (data to add kdj to)
        window: int (window size for kdj) Default: 9
        signal_window: int (window size for signal) Default: 3
    Returns:
        pd.DataFrame
    """
    result = data.ta.kdj(length=window, signal=signal_window)
    return _merge_indicator_result(data, result)


def add_know_sure_thing(data: pd.DataFrame) -> pd.DataFrame:
    """
    Add know sure thing to the data.
    
    Output columns: KST, KSTs (Signal)
    
    Args:
        data: pd.DataFrame (data to add know sure thing to)
    Returns:
        pd.DataFrame
    """
    result = data.ta.kst()
    return _merge_indicator_result(data, result)


def add_moving_average_convergence_divergence(data: pd.DataFrame, fast_length: int = 12, slow_length: int = 26, signal_length: int = 9) -> pd.DataFrame:
    """
    Add MACD to the data.
    
    Output columns: MACD (MACD Line), MACDh (Histogram), MACDs (Signal Line)
    
    Args:
        data: pd.DataFrame (data to add moving average convergence divergence to)
        fast_length: int (fast length for moving average convergence divergence) Default: 12
        slow_length: int (slow length for moving average convergence divergence) Default: 26
        signal_length: int (signal length for moving average convergence divergence) Default: 9
    Returns:
        pd.DataFrame
    """
    result = data.ta.macd(fast=fast_length, slow=slow_length, signal=signal_length)
    return _merge_indicator_result(data, result)


def add_momentum(data: pd.DataFrame, window: int = 1) -> pd.DataFrame:
    """
    Add momentum to the data.
    
    Output columns: MOM
    
    Args:
        data: pd.DataFrame (data to add momentum to)
        window: int (window size for momentum) Default: 1
    Returns:
        pd.DataFrame
    """
    result = data.ta.mom(length=window)
    return _merge_indicator_result(data, result)


def add_pretty_good_oscillator(data: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    """
    Add pretty good oscillator to the data.
    
    Output columns: PGO
    
    Args:
        data: pd.DataFrame (data to add pretty good oscillator to)
        window: int (window size for pretty good oscillator) Default: 14
    Returns:
        pd.DataFrame
    """
    result = data.ta.pgo(length=window)
    return _merge_indicator_result(data, result)


def add_percentage_price_oscillator(data: pd.DataFrame, fast_length: int = 12, slow_length: int = 26, signal_length: int = 9, scalar: float = 100) -> pd.DataFrame:
    """
    Add percentage price oscillator to the data.
    
    Output columns: PPO (PPO Line), PPOh (Histogram), PPOs (Signal Line)
    
    Args:
        data: pd.DataFrame (data to add percentage price oscillator to)
        fast_length: int (fast length for percentage price oscillator) Default: 12
        slow_length: int (slow length for percentage price oscillator) Default: 26
        signal_length: int (signal length for percentage price oscillator) Default: 9
        scalar: float (scalar for percentage price oscillator) Default: 100
    Returns:
        pd.DataFrame
    """
    result = data.ta.ppo(fast=fast_length, slow=slow_length, signal=signal_length, scalar=scalar)
    return _merge_indicator_result(data, result)


def add_psychological_line(data: pd.DataFrame, window: int = 12, scalar: float = 100) -> pd.DataFrame:
    """
    Add psychological line to the data.
    
    Output columns: PSL
    
    Args:
        data: pd.DataFrame (data to add psychological line to)
        window: int (window size for psychological line) Default: 12
        scalar: float (scalar for psychological line) Default: 100
    Returns:
        pd.DataFrame
    """
    result = data.ta.psl(length=window, scalar=scalar)
    return _merge_indicator_result(data, result)


def add_quantitative_qualitative_estimation(data: pd.DataFrame, window: int = 14, smooth_window: int = 5, factor: float = 4.236) -> pd.DataFrame:
    """
    Add quantitative qualitative estimation to the data.
    
    Output columns: QQE, QQEl (Long), QQEs (Short)
    
    Args:
        data: pd.DataFrame (data to add quantitative qualitative estimation to)
        window: int (window size for quantitative qualitative estimation) Default: 14
        smooth_window: int (window size for smooth) Default: 5
        factor: float (factor for quantitative qualitative estimation) Default: 4.236
    Returns:
        pd.DataFrame
    """
    result = data.ta.qqe(length=window, smooth=smooth_window, factor=factor)
    return _merge_indicator_result(data, result)


def add_rate_of_change(data: pd.DataFrame, window: int = 10, scalar: float = 100) -> pd.DataFrame:
    """
    Add rate of change to the data.
    
    Output columns: ROC
    
    Args:
        data: pd.DataFrame (data to add rate of change to)
        window: int (window size for rate of change) Default: 10
        scalar: float (scalar for rate of change) Default: 100
    Returns:
        pd.DataFrame
    """
    result = data.ta.roc(length=window, scalar=scalar)
    return _merge_indicator_result(data, result)


def add_relative_strength_index(data: pd.DataFrame, window: int = 14, scalar: float = 100) -> pd.DataFrame:
    """
    Add relative strength index to the data.
    
    Output columns: RSI
    
    Args:
        data: pd.DataFrame (data to add relative strength index to)
        window: int (window size for relative strength index) Default: 14
        scalar: float (scalar for relative strength index) Default: 100
    Returns:
        pd.DataFrame
    """
    result = data.ta.rsi(length=window, scalar=scalar)
    return _merge_indicator_result(data, result)


def add_relative_strength_xtra(data: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    """
    Add relative strength xtra to the data.
    
    Output columns: RSX
    
    Args:
        data: pd.DataFrame (data to add relative strength xtra to)
        window: int (window size for relative strength xtra) Default: 14
    Returns:
        pd.DataFrame
    """
    result = data.ta.rsx(length=window)
    return _merge_indicator_result(data, result)


def add_relative_vigor_index(data: pd.DataFrame, window: int = 14, swma_length: int = 4) -> pd.DataFrame:
    """
    Add relative vigor index to the data.
    
    Output columns: RVGI (RVGI Line), RVGIs (Signal Line)
    
    Args:
        data: pd.DataFrame (data to add relative vigor index to)
        window: int (window size for relative vigor index) Default: 14
        swma_length: int (window size for swma) Default: 4
    Returns:
        pd.DataFrame
    """
    result = data.ta.rvgi(length=window, swma_length=swma_length)
    return _merge_indicator_result(data, result)


def add_slope(data: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    """
    Add slope to the data.
    
    Output columns: SLOPE
    
    Args:
        data: pd.DataFrame (data to add slope to)
        window: int (window size for slope) Default: 14
    Returns:
        pd.DataFrame
    """
    result = data.ta.slope(length=window)
    return _merge_indicator_result(data, result)

def add_smart_money_concept(data: pd.DataFrame) -> pd.DataFrame:
    """
    Add smart money concept to the data.
    Args:
        data: pd.DataFrame (data to add smart money concept to)
    Returns:
        pd.DataFrame
    """
    result = data.ta.smc()
    return _merge_indicator_result(data, result)


def add_smi_ergodic_indicator(data: pd.DataFrame, fast_length: int = 5, slow_length: int = 20, signal_length: int = 5) -> pd.DataFrame:
    """
    Add SMI ergodic indicator to the data.
    
    Output columns: SMI, SMIs (Signal), SMIo (Oscillator)
    
    Args:
        data: pd.DataFrame (data to add smi ergodic indicator to)
        fast_length: int (fast length for smi ergodic indicator) Default: 5
        slow_length: int (slow length for smi ergodic indicator) Default: 20
        signal_length: int (signal length for smi ergodic indicator) Default: 5
    Returns:
        pd.DataFrame
    """
    result = data.ta.smi(fast=fast_length, slow=slow_length, signal=signal_length)
    return _merge_indicator_result(data, result)


def add_squeeze(data: pd.DataFrame, bb_length: int = 20, bb_std: float = 2.0, kc_length: int = 20, kc_scalar: float = 1.5) -> pd.DataFrame:
    """
    Add squeeze indicator to the data.
    
    Output columns: SQZ (Squeeze Momentum), SQZ_ON, SQZ_OFF, SQZ_NO
    
    Args:
        data: pd.DataFrame (data to add squeeze to)
        bb_length: int (Bollinger Band length) Default: 20
        bb_std: float (Bollinger Band std) Default: 2.0
        kc_length: int (Keltner Channel length) Default: 20
        kc_scalar: float (Keltner Channel scalar) Default: 1.5
    Returns:
        pd.DataFrame
    """
    result = data.ta.squeeze(bb_length=bb_length, bb_std=bb_std, kc_length=kc_length, kc_scalar=kc_scalar)
    return _merge_indicator_result(data, result)


def add_schaff_trend_cycle(data: pd.DataFrame, fast_length: int = 23, slow_length: int = 50, cycle_length: int = 10) -> pd.DataFrame:
    """
    Add schaff trend cycle to the data.
    
    Output columns: STC, STCmacd, STCstoch
    
    Args:
        data: pd.DataFrame (data to add schaff trend cycle to)
        fast_length: int (fast length for schaff trend cycle) Default: 23
        slow_length: int (slow length for schaff trend cycle) Default: 50
        cycle_length: int (cycle length for schaff trend cycle) Default: 10
    Returns:
        pd.DataFrame
    """
    result = data.ta.stc(fast=fast_length, slow=slow_length, k=cycle_length)
    return _merge_indicator_result(data, result)


def add_stochastic(data: pd.DataFrame, k: int = 14, d: int = 3, smooth_k: int = 3) -> pd.DataFrame:
    """
    Add stochastic oscillator to the data.
    
    Output columns: STOCHk (%K), STOCHd (%D), STOCHh (Histogram)
    
    Args:
        data: pd.DataFrame (data to add stochastic to)
        k: int (window size for stochastic) Default: 14
        d: int (window size for stochastic) Default: 3
        smooth_k: int (window size for smooth) Default: 3
    Returns:
        pd.DataFrame
    """
    result = data.ta.stoch(k=k, d=d, smooth_k=smooth_k)
    return _merge_indicator_result(data, result)


def add_fast_stochastic(data: pd.DataFrame, k: int = 14, d: int = 3) -> pd.DataFrame:
    """
    Add fast stochastic to the data.
    
    Output columns: STOCHFk (%K), STOCHFd (%D)
    
    Args:
        data: pd.DataFrame (data to add fast stochastic to)
        k: int (window size for fast stochastic) Default: 14
        d: int (window size for fast stochastic) Default: 3
    Returns:
        pd.DataFrame
    """
    result = data.ta.stochf(k=k, d=d)
    return _merge_indicator_result(data, result)


def add_stochastic_relative_strength_index(data: pd.DataFrame, window: int = 14, k: int = 3, d: int = 3, rsi_length: int = 14) -> pd.DataFrame:
    """
    Add stochastic RSI to the data.
    
    Output columns: STOCHRSIk (%K), STOCHRSId (%D)
    
    Args:
        data: pd.DataFrame (data to add stochastic relative strength index to)
        window: int (window size for stochastic relative strength index) Default: 14
        k: int (window size for stochastic relative strength index) Default: 3
        d: int (window size for stochastic relative strength index) Default: 3
        rsi_length: int (window size for rsi) Default: 14
    Returns:
        pd.DataFrame
    """
    result = data.ta.stochrsi(length=window, k=k, d=d, rsi_length=rsi_length)
    return _merge_indicator_result(data, result)


def add_true_momentum_oscillator(data: pd.DataFrame, tmo_length: int = 14, calc_length: int = 5, smooth_length: int = 3) -> pd.DataFrame:
    """
    Add true momentum oscillator to the data.
    
    Output columns: TMO, TMOs (Signal), TMOM, TMOMs
    
    Args:
        data: pd.DataFrame (data to add true momentum oscillator to)
        tmo_length: int (window size for true momentum oscillator) Default: 14
        calc_length: int (window size for calc) Default: 5
        smooth_length: int (window size for smooth) Default: 3
    Returns:
        pd.DataFrame
    """
    result = data.ta.tmo(tmo_length=tmo_length, calc_length=calc_length, smooth_length=smooth_length)
    return _merge_indicator_result(data, result)


def add_trix(data: pd.DataFrame, window: int = 18, signal_window: int = 9, scalar: float = 100) -> pd.DataFrame:
    """
    Add TRIX to the data.
    
    Output columns: TRIX, TRIXs (Signal)
    
    Args:
        data: pd.DataFrame (data to add trix to)
        window: int (window size for trix) Default: 18
        signal_window: int (window size for signal) Default: 9
        scalar: float (scalar for trix) Default: 100
    Returns:
        pd.DataFrame
    """
    result = data.ta.trix(length=window, signal=signal_window, scalar=scalar)
    return _merge_indicator_result(data, result)


def add_true_strength_index(data: pd.DataFrame, fast_length: int = 13, slow_length: int = 25, signal_length: int = 13, scalar: float = 100) -> pd.DataFrame:
    """
    Add true strength index to the data.
    
    Output columns: TSI, TSIs (Signal)
    
    Args:
        data: pd.DataFrame (data to add true strength index to)
        fast_length: int (fast length for true strength index) Default: 13
        slow_length: int (slow length for true strength index) Default: 25
        signal_length: int (signal length for true strength index) Default: 13
        scalar: int (scalar for true strength index) Default: 100
    Returns:
        pd.DataFrame
    """
    result = data.ta.tsi(fast=fast_length, slow=slow_length, signal=signal_length, scalar=scalar)
    return _merge_indicator_result(data, result)


def add_ultimate_oscillator(data: pd.DataFrame, fast: int = 7, medium: int = 14, slow: int = 28) -> pd.DataFrame:
    """
    Add ultimate oscillator to the data.
    
    Output columns: UO
    
    Args:
        data: pd.DataFrame (data to add ultimate oscillator to)
        fast: int (fast period) Default: 7
        medium: int (medium period) Default: 14
        slow: int (slow period) Default: 28
    Returns:
        pd.DataFrame
    """
    result = data.ta.uo(fast=fast, medium=medium, slow=slow)
    return _merge_indicator_result(data, result)


def add_williams_percent_r(data: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    """
    Add williams percent r to the data.
    
    Output columns: WILLR
    
    Args:
        data: pd.DataFrame (data to add williams percent r to)
        window: int (window size for williams percent r) Default: 14
    Returns:
        pd.DataFrame
    """
    result = data.ta.willr(length=window)
    return _merge_indicator_result(data, result)


# Indicator registry: maps indicator name (string) to its function
INDICATOR_REGISTRY = {
    # Momentum Indicators
    "ao": add_awesome_oscillator,
    "awesome_oscillator": add_awesome_oscillator,
    "apo": add_absolute_price_oscillator,
    "absolute_price_oscillator": add_absolute_price_oscillator,
    "bias": add_bias,
    "bop": add_balance_of_power,
    "balance_of_power": add_balance_of_power,
    "brar": add_br_and_ar,
    "br_ar": add_br_and_ar,
    "cci": add_commodity_channel_index,
    "commodity_channel_index": add_commodity_channel_index,
    "cfo": add_chande_forecast_oscillator,
    "chande_forecast_oscillator": add_chande_forecast_oscillator,
    "cg": add_center_of_gravity,
    "center_of_gravity": add_center_of_gravity,
    "cmo": add_chande_momentum_oscillator,
    "chande_momentum_oscillator": add_chande_momentum_oscillator,
    "coppock": add_coppock_curve,
    "coppock_curve": add_coppock_curve,
    "crsi": add_connors_relative_strength_index,
    "connors_rsi": add_connors_relative_strength_index,
    "cti": add_correlation_trend_indicator,
    "correlation_trend_indicator": add_correlation_trend_indicator,
    "dm": add_directional_movement,
    "directional_movement": add_directional_movement,
    "er": add_efficiency_ratio,
    "efficiency_ratio": add_efficiency_ratio,
    "eri": add_elder_ray_index,
    "elder_ray_index": add_elder_ray_index,
    "fisher": add_fisher_transform,
    "fisher_transform": add_fisher_transform,
    "inertia": add_inertia,
    "kdj": add_kdj,
    "kst": add_know_sure_thing,
    "know_sure_thing": add_know_sure_thing,
    "macd": add_moving_average_convergence_divergence,
    "moving_average_convergence_divergence": add_moving_average_convergence_divergence,
    "mom": add_momentum,
    "momentum": add_momentum,
    "pgo": add_pretty_good_oscillator,
    "pretty_good_oscillator": add_pretty_good_oscillator,
    "ppo": add_percentage_price_oscillator,
    "percentage_price_oscillator": add_percentage_price_oscillator,
    "psl": add_psychological_line,
    "psychological_line": add_psychological_line,
    "qqe": add_quantitative_qualitative_estimation,
    "roc": add_rate_of_change,
    "rate_of_change": add_rate_of_change,
    "rsi": add_relative_strength_index,
    "relative_strength_index": add_relative_strength_index,
    "rsx": add_relative_strength_xtra,
    "relative_strength_xtra": add_relative_strength_xtra,
    "rvgi": add_relative_vigor_index,
    "relative_vigor_index": add_relative_vigor_index,
    "slope": add_slope,
    "smc": add_smart_money_concept,
    "smart_money_concept": add_smart_money_concept,
    "smi": add_smi_ergodic_indicator,
    "smi_ergodic": add_smi_ergodic_indicator,
    "squeeze": add_squeeze,
    "sqz": add_squeeze,
    "stc": add_schaff_trend_cycle,
    "schaff_trend_cycle": add_schaff_trend_cycle,
    "stoch": add_stochastic,
    "stochastic": add_stochastic,
    "stochf": add_fast_stochastic,
    "fast_stochastic": add_fast_stochastic,
    "stochrsi": add_stochastic_relative_strength_index,
    "stochastic_rsi": add_stochastic_relative_strength_index,
    "tmo": add_true_momentum_oscillator,
    "true_momentum_oscillator": add_true_momentum_oscillator,
    "trix": add_trix,
    "tsi": add_true_strength_index,
    "true_strength_index": add_true_strength_index,
    "uo": add_ultimate_oscillator,
    "ultimate_oscillator": add_ultimate_oscillator,
    "willr": add_williams_percent_r,
    "williams_r": add_williams_percent_r,
    "williams_percent_r": add_williams_percent_r,
}


def _get_indicator_params(func) -> list[dict[str, Any]]:
    """
    Extract parameter information from an indicator function.
    
    Args:
        func: The indicator function
    
    Returns:
        List of parameter info dicts with name, default, and type
    """
    sig = inspect.signature(func)
    params = []
    
    for name, param in sig.parameters.items():
        # Skip 'data' parameter as it's always the DataFrame
        if name == 'data':
            continue
        
        param_info = {"name": name}
        
        # Get default value
        if param.default is not inspect.Parameter.empty:
            param_info["default"] = param.default
        
        # Get type annotation if available
        if param.annotation is not inspect.Parameter.empty:
            param_info["type"] = param.annotation.__name__ if hasattr(param.annotation, '__name__') else str(param.annotation)
        
        params.append(param_info)
    
    return params


def _get_indicator_description(func) -> str:
    """
    Extract short description from indicator function docstring.
    
    Args:
        func: The indicator function
    
    Returns:
        Short description string
    """
    if not func.__doc__:
        return ""
    
    # Get first non-empty line of docstring
    lines = func.__doc__.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line and not line.startswith('Output') and not line.startswith('Args'):
            return line
    return ""


def _get_indicator_output_columns(func) -> list[str]:
    """
    Extract output column names from indicator function docstring.
    
    Args:
        func: The indicator function
    
    Returns:
        List of output column names
    """
    if not func.__doc__:
        return []
    
    # Look for "Output columns:" line
    lines = func.__doc__.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('Output columns:'):
            # Extract column names after the colon
            cols_str = line.replace('Output columns:', '').strip()
            # Parse columns like "MACD, MACDh, MACDs" or "RSI"
            cols = [c.strip().split()[0] for c in cols_str.split(',')]
            return cols
    return []


def get_indicator_info(indicator: str) -> dict[str, Any]:
    """
    Get detailed information about a specific indicator.
    
    Args:
        indicator: Name of the indicator (case-insensitive)
    
    Returns:
        Dict with indicator information including:
        - name: Indicator name
        - description: Short description
        - parameters: List of parameters with name, default, and type
        - output_columns: List of column names that will be added
        - usage: Example usage string
    
    Raises:
        ValueError: If indicator is not found
    """
    indicator_lower = indicator.lower().strip()
    
    if indicator_lower not in INDICATOR_REGISTRY:
        available = ", ".join(sorted(set(INDICATOR_REGISTRY.keys())))
        raise ValueError(
            f"Unknown indicator: '{indicator}'. "
            f"Available indicators: {available}"
        )
    
    func = INDICATOR_REGISTRY[indicator_lower]
    params = _get_indicator_params(func)
    
    # Build usage example
    if params:
        param_examples = ", ".join([
            f"{p['name']}={p.get('default', '...')}" for p in params
        ])
        usage = f"{indicator_lower}({param_examples})"
    else:
        usage = indicator_lower
    
    return {
        "name": indicator_lower,
        "description": _get_indicator_description(func),
        "parameters": params,
        "output_columns": _get_indicator_output_columns(func),
        "usage": usage
    }


def get_available_indicators(detailed: bool = False) -> list[str] | list[dict[str, Any]]:
    """
    Get list of available indicators with optional detailed information.
    
    Args:
        detailed: If True, returns detailed info for each indicator.
                  If False, returns just the list of names.
    
    Returns:
        If detailed=False: List of indicator names
        If detailed=True: List of dicts with indicator info including:
            - name: Indicator name (short form)
            - description: Short description
            - parameters: List of {name, default, type}
            - output_columns: Columns that will be added to DataFrame
            - usage: Example usage string
    
    Examples:
        >>> get_available_indicators()
        ['ao', 'apo', 'bias', 'bop', ...]
        
        >>> get_available_indicators(detailed=True)
        [
            {
                "name": "rsi",
                "description": "Add relative strength index to the data.",
                "parameters": [{"name": "window", "default": 14, "type": "int"}, ...],
                "output_columns": ["RSI"],
                "usage": "rsi(window=14, scalar=100)"
            },
            ...
        ]
    """
    if not detailed:
        return sorted(set(INDICATOR_REGISTRY.keys()))
    
    # Get unique functions (avoid duplicates from aliases)
    seen_funcs = set()
    indicators_info = []
    
    for name in sorted(INDICATOR_REGISTRY.keys()):
        func = INDICATOR_REGISTRY[name]
        
        # Skip if we've already processed this function (alias)
        if id(func) in seen_funcs:
            continue
        seen_funcs.add(id(func))
        
        try:
            info = get_indicator_info(name)
            indicators_info.append(info)
        except Exception:
            # Skip if there's an error getting info
            continue
    
    return indicators_info


def _parse_indicator_string(indicator_str: str) -> tuple[str, dict]:
    """
    Parse indicator string with optional parameters.
    
    Supports formats:
        - "rsi" -> ("rsi", {})
        - "rsi(14)" -> ("rsi", {"window": 14})  # positional not supported, use named
        - "rsi(window=14)" -> ("rsi", {"window": 14})
        - "macd(fast=12, slow=26)" -> ("macd", {"fast": 12, "slow": 26})
        - "stochastic(k=14, d=3, smooth_k=3)" -> ("stochastic", {"k": 14, "d": 3, "smooth_k": 3})
    
    Args:
        indicator_str: Indicator string with optional parameters
    
    Returns:
        Tuple of (indicator_name, kwargs_dict)
    """
    indicator_str = indicator_str.strip()
    
    # Check if there are parameters
    match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.+)\)\s*$', indicator_str)
    
    if not match:
        # No parameters, just indicator name
        return indicator_str, {}
    
    indicator_name = match.group(1)
    params_str = match.group(2).strip()
    
    kwargs = {}
    
    # Parse key=value pairs
    # Handle: window=14, fast=12.5, smooth_k=3
    param_pattern = re.compile(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*([^,]+)')
    
    for param_match in param_pattern.finditer(params_str):
        key = param_match.group(1).strip()
        value_str = param_match.group(2).strip()
        
        # Try to convert value to appropriate type
        try:
            # Try int first
            if '.' not in value_str:
                value = int(value_str)
            else:
                value = float(value_str)
        except ValueError:
            # Keep as string if not a number
            value = value_str.strip('"\'')
        
        kwargs[key] = value
    
    return indicator_name, kwargs


def add_indicator(data: pd.DataFrame, indicator: str, **kwargs) -> pd.DataFrame:
    """
    Add an indicator to the data by name.
    
    Supports two ways to pass parameters:
    1. Via kwargs: add_indicator(data, "rsi", window=21)
    2. Via string: add_indicator(data, "rsi(window=21)")
    
    Args:
        data: pd.DataFrame (data to add indicator to)
        indicator: str (name of the indicator, case-insensitive, with optional params)
        **kwargs: Additional arguments to pass to the indicator function
    
    Returns:
        pd.DataFrame with indicator added
    
    Raises:
        ValueError: If indicator name is not recognized
    
    Examples:
        >>> data = add_indicator(data, "rsi")
        >>> data = add_indicator(data, "rsi(window=21)")
        >>> data = add_indicator(data, "macd(fast=12, slow=26, signal=9)")
        >>> data = add_indicator(data, "stochastic", k=14, d=3)
    """
    # Parse indicator string for embedded parameters
    indicator_name, parsed_kwargs = _parse_indicator_string(indicator)
    
    # Merge parsed kwargs with explicit kwargs (explicit takes precedence)
    merged_kwargs = {**parsed_kwargs, **kwargs}
    
    indicator_lower = indicator_name.lower().strip()
    
    if indicator_lower not in INDICATOR_REGISTRY:
        available = ", ".join(sorted(set(INDICATOR_REGISTRY.keys())))
        raise ValueError(
            f"Unknown indicator: '{indicator_name}'. "
            f"Available indicators: {available}"
        )
    
    indicator_func = INDICATOR_REGISTRY[indicator_lower]
    return indicator_func(data, **merged_kwargs)
